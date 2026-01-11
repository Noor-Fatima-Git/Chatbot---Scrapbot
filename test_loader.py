from rag.loader import load_text
from rag.chunker import chunk_text

text = load_text("data/notes.txt")
chunks = chunk_text(text)

print("Total chunks:", len(chunks))
print("\nFirst chunk:\n")
print(chunks[0])
