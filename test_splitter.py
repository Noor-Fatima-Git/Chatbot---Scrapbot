from rag.loader import load_text
from rag.splitter import split_text

text = load_text("data/notes.txt")
chunks = split_text(text)

print("Total chunks:", len(chunks))
print("\nFirst chunk:\n")
print(chunks[0])
