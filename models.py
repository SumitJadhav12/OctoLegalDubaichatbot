from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    question: str
    conversation_id: Optional[str] = None

class Citation(BaseModel):
    document: str
    section: str
    page: int
    source_url: str

class RetrievedPassage(BaseModel):
    text: str
    document: str
    section: str

class ChatResponse(BaseModel):
    answer: str
    status: str
    confidence: str = "medium"
    citations: List[Citation] = []
    retrieved_passages: List[RetrievedPassage] = []