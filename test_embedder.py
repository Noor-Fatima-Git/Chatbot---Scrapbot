from rag.loader import load_text
from rag.chunker import chunk_text
from rag.embedder import embed_chunks

text = load_text("data/notes.txt")
chunks = chunk_text(text)
embeddings = embed_chunks(chunks)

print("Chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)
