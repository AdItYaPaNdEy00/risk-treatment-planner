from services.chroma_client import add_documents, query_documents

# Step 1: Add documents
docs = [
    "System failure caused downtime",
    "Financial loss due to fraud",
    "Regulatory compliance issue detected"
]

add_documents(docs)

# Step 2: Query
query = "server crash problem"

results = query_documents(query)

print("Query:", query)
print("Results:", results["documents"])
