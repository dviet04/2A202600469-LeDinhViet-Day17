from chromadb import PersistentClient
from utils.config import CHROMA_DB_PATH

client = PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_or_create_collection("semantic")
all_docs = collection.get(include=['documents', 'ids', 'embeddings', 'metadatas'])

print("Tổng số documents:", len(all_docs['documents']))
for doc_id, doc in zip(all_docs['ids'], all_docs['documents']):
    print(f"ID: {doc_id} | Nội dung: {doc}")