from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import ChatRequest, ChatResponse
from rag import HybridRAG   # Updated import

app = FastAPI(
    title="OctoLegal UAE API",
    description="Citation-Grounded UAE Labour Law Chatbot",
    version="1.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG (Hybrid BM25 + Vector Search)
rag = HybridRAG()

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main endpoint for legal question answering.
    """
    result = rag.generate_response(request.question)
    return result

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "documents_loaded": len(rag.chunks),
        "retrieval_method": "Hybrid (BM25 + Vector Search)"
    }

# Optional: Add root endpoint for testing
@app.get("/")
async def root():
    return {
        "message": "OctoLegal UAE Labour Law Chatbot API is running!",
        "endpoints": {
            "chat": "POST /api/chat",
            "health": "GET /health"
        }
    }