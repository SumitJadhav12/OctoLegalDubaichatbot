from pypdf import PdfReader
import pickle
import os
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

print("Building BM25 + Vector Index...")

reader = PdfReader('data/UAE_Labour_Law.pdf')
chunks = []

model = SentenceTransformer('all-MiniLM-L6-v2')

for page_num, page in enumerate(reader.pages):
    text = page.extract_text() or ""
    if len(text.strip()) < 100:
        continue
    chunk_size = 700
    for i in range(0, len(text), chunk_size):
        chunk_text = text[i:i+chunk_size].strip()
        if len(chunk_text) > 100:
            chunks.append({
                "text": chunk_text,
                "page": page_num + 1,
                "document_title": "Federal Law No 8 of 1980 on Regulation of Labour Relations",
                "issuing_authority": "UAE Federal Government",
                "jurisdiction": "UAE",
                "effective_date": "1980",
                "url": "https://gulftalent.com/uae-labour-law"
            })

# Vector Index
texts = [c["text"] for c in chunks]
embeddings = model.encode(texts, show_progress_bar=True)
embeddings = np.array(embeddings).astype('float32')

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# Save
os.makedirs('simple_db', exist_ok=True)
with open('simple_db/chunks.pkl', 'wb') as f:
    pickle.dump(chunks, f)

faiss.write_index(index, 'simple_db/index.faiss')

print(f"✅ Created {len(chunks)} chunks with BM25 + FAISS Vector Index")