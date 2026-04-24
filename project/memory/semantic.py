
# SemanticMemory: ChromaDB + OpenAI Embedding
import os
from chromadb import PersistentClient
from chromadb.utils import embedding_functions
from utils.config import CHROMA_DB_PATH, OPENAI_API_KEY

class SemanticMemory:
    def __init__(self, collection_name="semantic"):
        self.client = PersistentClient(path=CHROMA_DB_PATH)
        self.collection = self.client.get_or_create_collection(collection_name)
        self.embed_fn = embedding_functions.OpenAIEmbeddingFunction(api_key=OPENAI_API_KEY)

    def add_document(self, doc_id: str, content: str):
        embedding = self.embed_fn([content])[0]
        self.collection.add(documents=[content], ids=[doc_id], embeddings=[embedding])

    def search(self, query: str, top_k=3):
        embedding = self.embed_fn([query])[0]
        results = self.collection.query(query_embeddings=[embedding], n_results=top_k)
        return results['documents'][0] if results['documents'] else []
