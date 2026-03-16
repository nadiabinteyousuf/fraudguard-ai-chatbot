# FraudGuard AI – Multi-Agent Fraud Detection Chatbot

Welcome! In this project, we build an intelligent fraud detection chatbot using modern AI tools. The chatbot can search the internet, analyze financial documents, detect suspicious transactions, and answer compliance questions from a knowledge base.

The goal of this project is to demonstrate how LLMs, agents, tools, and vector databases can work together in a real application.

## What You Will Learn

Through this project you will learn:

- How to connect an application to a Large Language Model (Gemini)
- How to design a multi-agent system
- How to implement Retrieval-Augmented Generation (RAG)
- How to use OCR to analyze financial documents
- How to build a chatbot UI using Streamlit
- How to monitor AI workflows using LangSmith

## Understanding the Architecture

Before looking at the code, let's understand how the system works.

The chatbot uses a Router Agent that decides which specialized agent should handle the user's request.

### System Workflow

```
User
 ↓
Streamlit Chat Interface
 ↓
Main Agent
 ↓
Router Agent
 ├── Search Agent
 ├── RAG Agent
 ├── OCR Agent
 └── Fraud Agent
 ↓
Gemini LLM
 ↓
Response to User
```

Each agent has a specific responsibility.

## Agents in the System

### Router Agent

The router agent decides which agent should process the user query.

**Example decisions:**

| User Query | Selected Agent |
|---|---|
| What are the latest cyber fraud trends? | Search Agent |
| What is FATF regulation? | RAG Agent |
| Extract text from this invoice | OCR Agent |
| Detect suspicious transactions | Fraud Agent |

### Search Agent

The search agent retrieves real-time information from the internet.

**Workflow:**

```
User Question
    ↓
Search Tool (Tavily)
    ↓
Web results collected
    ↓
Gemini summarizes results
    ↓
Answer returned with sources
```

**Example query:** What are the latest cyber fraud trends in 2026?

### RAG Agent

RAG stands for Retrieval-Augmented Generation.

Instead of answering from the model's training data, the system retrieves information from a custom knowledge base.

**Step 1 – Document Processing**

```
AML notes file
     ↓
Split into small chunks
     ↓
Convert each chunk to embeddings
     ↓
Store embeddings in FAISS vector database
```

**Step 2 – Question Answering**

```
User Question
     ↓
Convert question to embedding
     ↓
Find similar chunks from FAISS
     ↓
Send retrieved context to Gemini
     ↓
Generate answer based on context
```

**Example query:** What is FATF regulation?

### OCR Agent

The OCR agent extracts text from uploaded documents.

**Supported files:**

- PDF
- Images
- Bank statements
- Invoices
- Receipts

**Workflow:**

```
Uploaded Document
     ↓
OCR Tool (PyTesseract / PyMuPDF)
     ↓
Extracted Text
     ↓
Fraud analysis or text output
```

**Example query:** Extract text from this invoice

### Fraud Detection Agent

The fraud agent analyzes suspicious financial activity.

It checks patterns such as:

- Structuring (many small transfers)
- Sanctions screening
- Suspicious transaction amounts
- Unusual patterns in bank statements

**Example query:** I received multiple small transfers of $450. Is this suspicious?

## Key Concepts

### Embeddings

Embeddings convert text into numerical vectors that represent meaning.

**Example:**
```
"I am happy"
"I feel joyful"
```

These sentences produce similar embeddings because they have similar meaning.

In this project we use: `sentence-transformers/all-MiniLM-L6-v2`

### FAISS Vector Database

FAISS stores embeddings and allows fast similarity search.

When a question is asked:

- The question is converted into an embedding
- FAISS finds similar document chunks
- Those chunks are sent to the LLM as context

### LangSmith Tracing

LangSmith tracks the execution of AI agents.

It records:

- Agent calls
- Tool usage
- Response latency
- Errors

**Example trace:**
```
main_agent
 ↓
router_agent
 ↓
search_agent
```

This helps debug and monitor the AI workflow.

## Project Structure

```
fraudguard-ai-chatbot/
├── backend/
│   ├── .env
│   ├── __init__.py
│   ├── config.py
│   ├── test_router.py
│   ├── agent/
│   │   ├── fraud_agent.py
│   │   ├── gemini_client.py
│   │   ├── main_agent.py
│   │   ├── ocr_agent.py
│   │   ├── rag_agent.py
│   │   ├── router_agent.py
│   │   ├── search_agent.py
│   │   └── __init__.py
│   ├── prompts/
│   │   ├── fraud_prompt.py
│   │   ├── rag_prompt.py
│   │   ├── router_prompt.py
│   │   ├── search_prompt.py
│   │   └── __init__.py
│   ├── rag/
│   │   ├── build_index.py
│   │   ├── vector_store.py
│   │   └── __init__.py
│   ├── tools/
│   │   ├── ocr_tool.py
│   │   ├── search_tool.py
│   │   └── __init__.py
│   └── venv/
├── data/
├── faiss_index/
├── frontend/
│   └── app.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Tech Stack

| Component | Tool |
|---|---|
| LLM | Google Gemini (gemini-2.5-flash) |
| Framework | LangChain |
| Vector Database | FAISS |
| Embeddings | sentence-transformers |
| OCR | PyTesseract + PyMuPDF |
| Frontend | Streamlit |
| Monitoring | LangSmith |
| Search Tool | Tavily |

## Setup Instructions

### Step 1 – Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/fraudguard-ai-chatbot.git
cd fraudguard-ai-chatbot
```

### Step 2 – Create Virtual Environment

```bash
python -m venv venv
```

**Activate it:**

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### Step 3 – Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 – Add API Keys

Create `.env` file:

```
GEMINI_API_KEY=your_gemini_key
TAVILY_API_KEY=your_search_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_PROJECT=FraudGuard-AI
```

### Step 5 – Run the Application

```bash
streamlit run app.py
```

Open browser: `http://localhost:8501`

---

