from rag.loader import load_text
from rag.chunker import chunk_text
from rag.embedder import embed_chunks
from rag.search import search

# load + prepare data
text = load_text("data/notes.txt")
chunks = chunk_text(text)
chunk_embeddings = embed_chunks(chunks)

# ask a question
question = "What is this document about?"
question_embedding = embed_chunks([question])[0]

# search
result = search(question_embedding, chunk_embeddings, chunks)

print("Answer from document:\n")
print(result)
