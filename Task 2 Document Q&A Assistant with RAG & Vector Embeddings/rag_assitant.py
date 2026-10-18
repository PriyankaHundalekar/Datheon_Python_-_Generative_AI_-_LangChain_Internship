import os
import sys
import time
from pathlib import Path
from google import genai
from google.genai import types
from google.genai.errors import ClientError
from dotenv import load_dotenv
import chromadb
from pypdf import PdfReader

# Load environment variables
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY could not be loaded from the .env file!")

# Initialize Gemini client
client = genai.Client(api_key=api_key)

# Initialize local ChromaDB vector database
db_path = Path(__file__).resolve().parent / "chroma_db"
chroma_client = chromadb.PersistentClient(path=str(db_path))
collection_name = "policy_manual_43_pages_collection"

# Get or create collection
collection = chroma_client.get_or_create_collection(name=collection_name)


def get_embedding_with_retry(text: str, max_retries: int = 4) -> list[float]:
    """Generates embeddings using Google's cloud model with 429 rate-limit backoff."""
    delay = 6.0
    for attempt in range(max_retries):
        try:
            response = client.models.embed_content(
                model="models/gemini-embedding-2",
                contents=text,
            )
            return response.embeddings[0].values
        except ClientError as e:
            if getattr(e, "code", None) == 429 or "429" in str(e):
                if attempt == max_retries - 1:
                    print(f"\n[Rate Limit Exhausted] Max retries reached.")
                    raise e
                print(f"\n[Rate limit 429 hit] Pausing for {delay} seconds before retry {attempt+1}/{max_retries}...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                raise e


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts text page by page from a large PDF file."""
    reader = PdfReader(pdf_path)
    full_text = ""
    print(f"Parsing {len(reader.pages)} pages from PDF...")
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            full_text += f"\n--- Page {i+1} ---\n" + text
    return full_text


def ingest_pdf_document(file_path: str):
    """Reads the 43-page PDF, chunks it, embeds it with Google Cloud, and stores it."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Check if database already has chunks stored (Caching)
    existing_count = collection.count()
    if existing_count > 0:
        print(f"Vector database already contains {existing_count} chunks. Skipping re-ingestion!")
        return

    print(f"Reading and parsing 43-page PDF: {path.name}...")
    full_text = extract_text_from_pdf(str(path))

    # Split text into clean paragraph chunks (filtering out tiny lines)
    raw_chunks = full_text.split("\n\n")
    chunks = [chunk.strip() for chunk in raw_chunks if len(chunk.strip()) > 40]
    
    print(f"Extracted {len(chunks)} valid text chunks. Generating Google Cloud embeddings...")
    print("Note: Processing a 43-page document may take a couple of minutes to safely respect rate limits.")

    ids = []
    embeddings = []
    documents = []

    for i, chunk in enumerate(chunks):
        chunk_id = f"{path.stem}_chunk_{i}"
        
        print(f"[{i+1}/{len(chunks)}] Embedding chunk via Google API...")
        vector = get_embedding_with_retry(chunk)
        
        ids.append(chunk_id)
        embeddings.append(vector)
        documents.append(chunk)
        
        # Pacing buffer between chunks to maintain quota health
        time.sleep(2.5)

    # Upsert into ChromaDB in batches
    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=documents
    )
    print(f"\nSuccessfully ingested all {len(chunks)} chunks into ChromaDB!")


def query_rag_assistant(user_query: str) -> str:
    """Retrieves context locally and forces Gemini to answer STRICTLY from the PDF chunks."""
    print(f"\nSearching vector database for: '{user_query}'...")
    
    # 1. Embed query using Google cloud model with retry
    query_vector = get_embedding_with_retry(user_query)

    # 2. Query ChromaDB for top 3 matching chunks
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=3
    )

    retrieved_chunks = results["documents"][0]
    
    if not retrieved_chunks:
        return "I cannot find the answer in the provided documents."

    # --- VISUAL VERIFICATION (Proof that it comes from the PDF) ---
    print("\n🔍 [Debug] Exact Text Chunks Retrieved from PDF:")
    for idx, chunk in enumerate(retrieved_chunks):
        print(f"  -> Chunk {idx+1} preview: {chunk[:150].strip()}...")
    print("-" * 50)

    context_text = "\n\n---\n\n".join(retrieved_chunks)

    # --- STRICT GROUNDING PROMPT ---
    prompt = f"""
    You are a strict enterprise compliance assistant. Your task is to answer the user's question 
    SOLELY based on the provided context extracted from the company policy manual PDF.

    CRITICAL INSTRUCTIONS:
    1. Base your answer ONLY on the explicit facts present in the Context below.
    2. Do NOT use any external knowledge, general assumptions, or prior training data.
    3. If the answer cannot be found entirely within the provided context, you MUST output verbatim: 
       "I cannot find the answer in the provided documents."
    4. Do not extrapolate, guess, or fill in gaps with outside information.

    Context:
    {context_text}

    User Question: {user_query}
    """

    # Generate response using Gemini Flash with temperature 0.0 (zero hallucination)
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.0  # Zero creativity ensures strict adherence to text
        ),
    )

    return response.text


# --- Interactive Terminal Execution ---
if __name__ == "__main__":
    # Pointing directly to your 43-page PDF using a raw string
    target_pdf = r"D:\Microsoft_VS_Code\Datheon_Internship\Task 2 Document Q&A Assistant with RAG & Vector Embeddings\04-Policy-Manual-Apr-2016-excl-SAICA.pdf"

    # Step 1: Ingest the 43-page PDF using Google embeddings (runs once, then caches)
    ingest_pdf_document(target_pdf)

    print("\n" + "="*50)
    print("🤖 43-Page Policy RAG Assistant is ready! Ask anything about your manual.")
    print("Type 'exit' or 'quit' to stop.")
    print("="*50 + "\n")

    while True:
        user_query = input("Ask a question: ").strip()
        if user_query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        if not user_query:
            continue

        answer = query_rag_assistant(user_query)
        print(f"\nAnswer:\n{answer}\n" + "-"*50)