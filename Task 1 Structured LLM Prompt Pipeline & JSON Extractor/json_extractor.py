import os
import sys
from pathlib import Path
from typing import List, Optional
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY could not be loaded from the .env file!")

client = genai.Client(api_key=api_key)


# --- Schemas for Both Invoice and Resume ---
class LineItem(BaseModel):
    description: str = Field(description="Description of item/service")
    quantity: int = Field(description="Quantity")
    unit_price: float = Field(description="Unit price")
    total_price: float = Field(description="Total price")

class InvoiceSchema(BaseModel):
    vendor_name: str = Field(description="Name of the vendor issuing the invoice")
    invoice_date: Optional[str] = Field(description="Invoice date YYYY-MM-DD")
    line_items: List[LineItem] = Field(description="List of purchased items")
    grand_total: float = Field(description="Final total amount due")

class ResumeSchema(BaseModel):
    full_name: str = Field(description="Candidate's full name")
    email: Optional[str] = Field(description="Candidate's email address")
    phone_number: Optional[str] = Field(description="Candidate's phone number")
    skills: List[str] = Field(description="List of technical and professional skills")
    current_role: Optional[str] = Field(description="Current or most recent job title")
    total_experience_years: Optional[float] = Field(description="Estimated total years of experience")


def extract_data_from_file(file_path: str):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    print(f"Uploading file '{path.name}' to Gemini API...")
    
    # Upload the file using the Gemini Files API (handles PDFs, PNGs, JPEGs natively)
    uploaded_file = client.files.upload(file=str(path))
    
    # Determine schema and prompt based on filename/type
    if "invoice" in path.name.lower() or path.suffix.lower() in [".png", ".jpg", ".jpeg"]:
        print("Detected Invoice/Receipt document. Extracting financial schema...")
        schema = InvoiceSchema
        prompt = "Extract the structured invoice details from this document strictly matching the requested schema."
    else:
        print("Detected Resume document. Extracting professional candidate schema...")
        schema = ResumeSchema
        prompt = "Extract the structured resume details from this document strictly matching the requested schema."

    # Generate content using the uploaded file reference
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=[uploaded_file, prompt],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=schema,
            temperature=0.1,
        ),
    )

    # Validate and return structured JSON matching the appropriate schema
    structured_data = schema.model_validate_json(response.text)
    
    # Clean up the uploaded file from Google's servers after processing
    client.files.delete(name=uploaded_file.name)
    
    return structured_data


if __name__ == "__main__":
    # Pass the filename as an argument in the terminal, or default to your files
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
    else:
        # Default prompt user or pick one of your files
        #target_file = "D:\Microsoft_VS_Code\Datheon_Internship\Task 1 Structured LLM Prompt Pipeline & JSON Extractor\gst-invoice-bill.png" # You can change this to your PDF resume filename
        target_file = "D:\Microsoft_VS_Code\Datheon_Internship\Task 1 Structured LLM Prompt Pipeline & JSON Extractor\Priyanka Mohan Hundalekar Resume.pdf" # You can change this to your PDF resume filename
    
    print(f"\nProcessing target file: {target_file}\n" + "-"*40)
    result = extract_data_from_file(target_file)
    
    print("\nExtracted Structured Output:\n")
    print(result.model_dump_json(indent=2))