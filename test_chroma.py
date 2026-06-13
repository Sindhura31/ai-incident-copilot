import chromadb

client = chromadb.Client()
collection = client.create_collection("test")

collection.add(
    documents=[
        "VPN authentication failure requires checking MFA provider status",
        "Database connectivity issues require checking connection pool settings",
        "Application crash requires reviewing error logs and memory usage"
    ],
    ids=["doc1", "doc2", "doc3"]
)

results = collection.query(
    query_texts=["users cannot login via VPN"],
    n_results=2
)

print("Top matches:")
for doc in results["documents"][0]:
    print("-", doc)