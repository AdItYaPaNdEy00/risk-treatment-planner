import chromadb
import uuid
from chromadb.utils import embedding_functions

# Persistent DB path
CHROMA_PATH = "chroma_data"

# Embedding model
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Initialize client (persistent)
client = chromadb.PersistentClient(path=CHROMA_PATH)

# Create/get collection
collection = client.get_or_create_collection(
    name="risk_collection",
    embedding_function=embedding_function
)


def add_documents(docs: list):
    import uuid

    global collection

    # delete and recreate collection (clean reset)
    client.delete_collection(name="risk_collection")

    collection = client.get_or_create_collection(
        name="risk_collection",
        embedding_function=embedding_function
    )

    ids = [str(uuid.uuid4()) for _ in docs]

    collection.add(
        documents=docs,
        ids=ids
    )


def query_documents(query: str, n_results: int = 2):
    """
    Query similar documents
    """
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    return results