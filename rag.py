import pickle
import re
import faiss
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

class HybridRAG:
    def __init__(self):
        with open('simple_db/chunks.pkl', 'rb') as f:
            self.chunks = pickle.load(f)
        
        self.index = faiss.read_index('simple_db/index.faiss')
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # BM25
        tokenized = [chunk["text"].split() for chunk in self.chunks]
        self.bm25 = BM25Okapi(tokenized)

    def retrieve(self, query: str, k: int = 4):
        # Vector Search
        query_vec = self.model.encode([query]).astype('float32')
        _, vec_idx = self.index.search(query_vec, k)
        
        # BM25 Search
        bm25_scores = self.bm25.get_scores(query.split())
        bm25_idx = np.argsort(bm25_scores)[-k:]

        # Hybrid combination
        combined_idx = set(vec_idx[0]) | set(bm25_idx)
        candidates = [self.chunks[i] for i in combined_idx if i < len(self.chunks)]
        
        return candidates[:k]

    def _extract_article(self, text):
        match = re.search(r'Article\s+(\d+)', text, re.IGNORECASE)
        return f"Article {match.group(1)}" if match else f"Page {text[:100].find('Section') or 'Relevant'}"

    def generate_response(self, query: str):
        passages = self.retrieve(query)
        
        if not passages:
            return {
                "answer": "I could not find sufficient support in the available documents.",
                "status": "insufficient_evidence",
                "citations": [],
                "retrieved_passages": []
            }

        answer = "**Answer based on UAE Labour Law (Hybrid BM25 + Vector Search):**\n\n"
        for i, p in enumerate(passages, 1):
            article = self._extract_article(p["text"])
            clean_text = re.sub(r'\s+', ' ', p["text"]).strip()[:600]
            answer += f"**{i}. {article}**\n{clean_text}...\n\n"

        answer += "**Note:** This is general legal information only."

        citations = [{
            "document": p["document_title"],
            "section": self._extract_article(p["text"]),
            "page": p['page'],
            "source_url": p.get("url", "")
        } for p in passages]

        retrieved = [{
            "text": re.sub(r'\s+', ' ', p["text"])[:650],
            "document": p["document_title"],
            "section": self._extract_article(p["text"])
        } for p in passages]

        return {
            "answer": answer,
            "status": "answered",
            "confidence": "high",
            "citations": citations,
            "retrieved_passages": retrieved
        }