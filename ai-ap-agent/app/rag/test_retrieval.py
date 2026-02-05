from app.rag.retriever import retrieve_policy

query = "What should happen if vendor bank details change?"

results = retrieve_policy(query)

print("\n🔍 Query:", query)

for r in results:
    print("\n✅ Source:", r["source"])
    print(r["content"][:300])
