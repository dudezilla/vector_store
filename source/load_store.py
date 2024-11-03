import faiss
from uuid import uuid4
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

new_vector_store = FAISS.load_local(
    "faiss_index", embeddings, allow_dangerous_deserialization=True
)
