import os
import faiss
from sentence_transformers import SentenceTransformer

# ✅ Load embedding model (fast on CPU)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Paths
KNOWLEDGE_FOLDER = "knowledge"
INDEX_FILE = "data/policy_index.faiss"

documents = []

# ✅ Load all policy documents
for filename in os.listdir(KNOWLEDGE_FOLDER):
    filepath = os.path.join(KNOWLEDGE_FOLDER, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        documents.append(f.read())

print("✅ Loaded documents:", len(documents))

# ✅ Convert documents → embeddings
embeddings = model.encode(documents)

# ✅ Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# ✅ Save index to disk
faiss.write_index(index, INDEX_FILE)

print("✅ Policy Index Created Successfully!")
print("Saved at:", INDEX_FILE)
