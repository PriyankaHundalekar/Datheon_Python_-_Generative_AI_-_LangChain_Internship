
# Datheon Python, Generative AI & LangChain Portfolio

A portfolio of three Python-based Generative AI projects developed as part of the Datheon Python, Generative AI & LangChain Internship program. The projects explore structured LLM output generation, Retrieval-Augmented Generation (RAG), semantic document search, and tool-using AI agents.

The goal of this portfolio is to demonstrate practical application engineering with large language models (LLMs), including prompt design, data validation, retrieval pipelines, external tool integration, and traceable execution.

## Projects at a Glance

| Project | Core Capability | Key Technologies |
|---|---|---|
| Task 1: Structured LLM Prompt Pipeline & JSON Extractor | Extract structured information from unstructured text | Python, Google Gemini API, JSON |
| Task 2: Document Q&A Assistant with RAG | Answer document questions using retrieved context | Python, embeddings, LangChain/RAG utilities, vector store |
| Task 3: Multi-Tool Autonomous AI Agent | Use tools to solve multi-step queries | Python, Gemini, DuckDuckGo Search, calculator, file reader |

## Task 1: Structured LLM Prompt Pipeline & JSON Extractor

### Overview

This project demonstrates how an LLM can transform unstructured text into machine-readable JSON. It uses Google's Gemini API to interpret input content and produce structured information according to a defined output format.

The pipeline is designed to separate prompt construction, model interaction, response parsing, and output validation, making the extraction workflow easier to test, maintain, and extend.

### Key Capabilities

- **Structured information extraction:** Convert unstructured text into predefined fields.
- **Prompt engineering:** Organize instructions and input data using reusable prompt templates.
- **LLM integration:** Connect Python applications to the Gemini API.
- **JSON processing:** Parse model responses into a machine-readable format.
- **Validation and error handling:** Check output structure and handle malformed or incomplete responses where implemented.
- **Extensibility:** Adapt the extraction schema to use cases such as resume parsing, invoice processing, and document metadata extraction.

### Processing Workflow

1. Accept input text or document content.
2. Construct a prompt containing the extraction instructions and expected output structure.
3. Send the prompt to the Gemini API.
4. Receive and parse the generated response.
5. Validate the output against the expected schema, if configured.
6. Return the structured JSON result for downstream processing.

### Architecture
<p align="center">
  <img src="JSON%20Extractor.jpg" alt="JSON Extractor Architecture" width="800">
</p>

<img width="630" height="220" alt="6" src="https://github.com/user-attachments/assets/da2a6613-4ea4-4e98-b8fb-9e603061cb10" />


### Practical Applications

Resume information extraction, invoice field extraction, document classification, and converting unstructured business information into structured records.

---

## Task 2: Document Q&A Assistant with RAG & Vector Embeddings

### Overview

This project implements a Retrieval-Augmented Generation workflow that enables users to ask questions about their own documents. Instead of relying solely on the LLM's pre-trained knowledge, the application retrieves relevant passages from an indexed document collection and uses that evidence to formulate a response.

The retrieval pipeline connects document processing, semantic search, and LLM-based answer generation.

### Key Capabilities

- **Document ingestion:** Load supported PDF or text documents.
- **Text chunking:** Split lengthy content into smaller passages suitable for embedding and retrieval.
- **Vector embeddings:** Represent text chunks as numerical vectors for semantic similarity search.
- **Vector storage:** Index embeddings and associated document metadata in the configured vector store.
- **Contextual retrieval:** Retrieve passages relevant to the user's query.
- **Grounded answer generation:** Provide retrieved context to the LLM when generating an answer.
- **Source attribution:** Preserve and display source-page or document references where supported by the implementation.

### Processing Workflow

1. Load the supported documents.
2. Extract text and preserve relevant metadata, such as page numbers.
3. Split the text into manageable chunks.
4. Generate embeddings for the chunks.
5. Store the vectors and metadata in the configured vector database.
6. Embed the user's question and retrieve relevant chunks.
7. Construct a context-aware prompt using the retrieved evidence.
8. Generate an answer and present available source references.

### Architecture
<img width="800" height="800" alt="2" src="https://github.com/user-attachments/assets/2e375aa7-8f41-4165-9e96-4b4c386113c2" />


<img width="777" height="427" alt="4" src="https://github.com/user-attachments/assets/22c9eed7-3848-458c-ae0c-974976ac40e3" />


### Practical Applications

Internal knowledge assistants, policy and documentation search, research-paper Q&A, report analysis, and document-based customer support.

---

## Task 3: Multi-Tool Autonomous AI Agent

### Overview

This project explores tool-using AI agents that can select and invoke external functions to address user queries. The agent combines an LLM with a set of tools for web search, mathematical calculations, and local file reading.

Rather than relying on a single model response for every task, the workflow allows the agent to use tool results as additional evidence before producing its final answer.

### Available Tools

- **`web_search`:** Retrieve relevant information from web search results using the configured search integration.
- **`python_calculator`:** Perform mathematical calculations through Python-based execution.
- **`local_file_reader`:** Read permitted local files and provide their contents for analysis.

### Key Capabilities

- **Tool integration:** Expose Python functions through a consistent tool interface.
- **Tool selection:** Allow the LLM to select an appropriate tool for a query.
- **Multi-step execution:** Use tool results to inform subsequent steps when necessary.
- **Execution logging:** Record tool invocations, inputs, outputs, and execution status where implemented.
- **Response synthesis:** Combine the user's request with tool observations to generate a final response.
- **Extensibility:** Add new tools without redesigning the entire application.

### Processing Workflow

1. Receive a user query.
2. Send the query and available tool descriptions to the agent.
3. Determine whether a tool is required.
4. Invoke the selected tool and capture its result.
5. Provide the observation back to the agent for further processing.
6. Repeat within configured execution limits if additional actions are needed.
7. Generate the final answer based on the available evidence.

### Architecture

<img width="3309" height="1870" alt="3" src="https://github.com/user-attachments/assets/5d6172ac-a10f-458a-a562-00173f95e648" />


<img width="577" height="617" alt="5" src="https://github.com/user-attachments/assets/d13b65c1-dfe2-4c5f-826c-6560ed1d431b" />


### Practical Applications

Research assistants, document-analysis workflows, calculation-enabled chatbots, and assistants that combine external information with local data.

---

## Technology Stack

- **Language:** Python 3
- **LLM integration:** Google GenAI SDK (`google-genai`)
- **Structured data:** JSON; schema validation where implemented
- **Retrieval and orchestration:** LangChain and RAG utilities, as applicable to each project
- **Vector search:** The configured vector store and embedding implementation
- **Web search:** DuckDuckGo Search (`ddgs`)
- **Application interfaces:** FastAPI and/or Streamlit where used

## Repository Structure

```text
# Datheon Python, Generative AI & LangChain Internship Portfolio

Welcome to my official portfolio repository! This repository showcases the complete implementation, system architecture, and empirical verification of advanced Generative AI applications, structured prompt engineering pipelines, Retrieval-Augmented Generation (RAG) Q&A systems, and multi-tool autonomous AI agents built during the Datheon Internship program.

---

## 📂 Project Directory Structure

```text
Datheon_Internship/
├── Task 1 Structured LLM Prompt Pipeline & JSON Extractor/
│   ├── Outputs/
│   │   ├── Invoice Output 1.png
│   │   ├── Invoice Output 2.png
│   │   └── Resume Analysis Output.png
│   ├── gst-invoice-bill.png
│   ├── Priyanka Mohan Hundalekar Resume.pdf
│   ├── json_extractor.py
│   └── requirements.txt
│
├── Task 2 Document Q&A Assistant with RAG & Vector Embeddings/
│   ├── chroma_db/
│   ├── Outputs/
│   │   ├── Evaluating RAG Question in Out of Scope 3.png
│   │   ├── Evaluating RAG Question in Scope 1.png
│   │   ├── Evaluating RAG Question in Scope 2.png
│   │   ├── Testing RAG Application.png
│   │   ├── Vector Embeddings 1.png
│   │   └── Vector Embeddings 2.png
│   ├── 04-Policy-Manual-Apr-2016-excl-SAICA.pdf
│   └── evaluate_rag.py
│
├── Task 3 Multi-Tool Autonomous AI Agent/
│   ├── Outputs/
│   │   ├── Tool 1 Reading vlaues from text file .png
│   │   ├── Tool 1 Total of vlaues from text file .png
│   │   ├── Tool 2 Python Calculator 1.png
│   │   ├── Tool 2 Python Calculator 2.png
│   │   ├── Tool 2 Python Calculator 3.png
│   │   └── Tool 3 Web Search 1.png
│   ├── company_budget.txt
│   └── autonomous_agent.py
│
├── .env.example
└── README.md
```

The folder names above represent the proposed organization. Preserve the actual file names and directory structure of your existing implementation when updating the README.

## Setup and Configuration

1. Install Python 3 and create a virtual environment.
2. Install each project's dependencies using its supplied `requirements.txt`, if present.
3. Configure the required API credentials through environment variables.
4. Follow the setup instructions in the corresponding project directory.
5. Run each application using its documented entry point.

Never commit API keys, private documents, or other sensitive information to a public repository.

## Learning Outcomes

Through these projects, the portfolio demonstrates practical work with:

- LLM API integration and prompt engineering
- Structured output generation and JSON processing
- Document ingestion, chunking, embeddings, and vector retrieval
- Retrieval-Augmented Generation workflows
- LLM tool calling and agent orchestration
- Error handling, execution logging, and modular Python development

## Future Improvements

Potential extensions include automated evaluation datasets, improved retrieval ranking, stronger schema validation, configurable model selection, latency and token-cost monitoring, expanded automated testing, and deployment with appropriate access controls.

---

**Author:** Priyanka Mohan Hundalekar  
**Program:** Datheon Python, Generative AI & LangChain Internship  
**Focus Areas:** Python, Generative AI, RAG, LLM applications, and AI agents
