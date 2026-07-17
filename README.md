# OctoLegal Dubai - Citation Grounded Legal Chatbot

## Selected Domain
Employment Regulations (UAE Federal Labour Law)

## Documents Used
- Title: Federal Law No 8 of 1980 on Regulation of Labour Relations
- Authority: UAE Federal Government
- Year: 1980
- Jurisdiction: UAE

## How to Run
1.  pip install -r requirements.txt`
2.  python ingest.py`
3.  uvicorn main:app --reload --port 8000 
4. `streamlit run app.py`

## Fulfilled Requirements
- Document ingestion with metadata
- Citation-grounded answers
- Refusal behavior
- Conversation context
- Clear distinction between info and advice
- Simple UI with source excerpts

## Features
- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Metadata-based Document Retrieval
- Citation Grounding
- Conversation Memory
- Hallucination Prevention
- Refusal for Unsupported Questions
- FastAPI REST API
- Streamlit User Interface
- Source Excerpts
- Document Metadata Display
- Multi-turn Conversation Support
## Simple UI
The Streamlit application provides

- Chat Interface
- Source Excerpts
- Retrieved Document Sections
- Conversation History
- Clear Citation Display
- User-friendly Design
## FUllfilled Requirements
Document ingestion with metadata
- Retrieval-Augmented Generation (RAG)
- Citation-grounded answers
- Hallucination mitigation
- Refusal behavior
- Conversation memory
- Semantic search
- Metadata filtering
- Source excerpt display
- Clear distinction between legal information and legal advice
- FastAPI backend
- Streamlit frontend
- Vector database integration
- Production-ready project structure
- Hybrid Search BM25 + vector index
## Project Architecture
User Question
       │
       ▼
 Streamlit UI
       │
       ▼
 FastAPI Backend
       │
       ▼
Query Embedding
       │
       ▼
Vector Database (FAISS / ChromaDB)
       │
Retrieve Relevant Chunks
       │
       ▼
Prompt + Retrieved Context
       │
       ▼
Large Language Model
       │
       ▼
Citation-Grounded Response
## Technolgies used
## Backend
- Python
- FastAPI
- Uvicorn
## Frontend
Streamlit


