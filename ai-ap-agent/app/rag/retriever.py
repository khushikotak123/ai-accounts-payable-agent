import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model (same one used in indexing)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Paths
INDEX_FILE = "data/policy_index.faiss"
KNOWLEDGE_FOLDER = "knowledge"

# Load FAISS index
index = faiss.read_index(INDEX_FILE)

# Load documents into memory
documents = []
filenames = []

for file in os.listdir(KNOWLEDGE_FOLDER):
    with open(os.path.join(KNOWLEDGE_FOLDER, file), "r", encoding="utf-8") as f:
        documents.append(f.read())
        filenames.append(file)


def retrieve_policy(query: str, top_k: int = 2):
    """
    Retrieve most relevant policy documents for a query.
    """

    # Convert query to embedding
    query_embedding = model.encode([query])

    # Search FAISS
    distances, indices = index.search(np.array(query_embedding), top_k)

    results = []
    for idx in indices[0]:
        results.append(
            {
                "source": filenames[idx],
                "content": documents[idx]
            }
        )

    return results
