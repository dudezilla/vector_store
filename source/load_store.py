from langsmith import traceable

from langchain.storage import LocalFileStore
from langchain_community.document_loaders import TextLoader

from langchain_community.vectorstores import FAISS
from langchain.embeddings import CacheBackedEmbeddings
from langchain_nomic import NomicEmbeddings
from langchain_text_splitters import CharacterTextSplitter

import json
from file_wrapper import File_Wrapper
from file_collection import File_Collection
import os

def load_config():
    with open("config.json","r") as f:
        str = f.read()
    CONFIG = json.loads(str)
    return CONFIG


def init():
    result = load_config()
    result['UNDERLYING_EMBEDDINGS'] = NomicEmbeddings(
        model=result['EMBEDDING_MODEL'],
        # dimensionality=256,
        # Nomic's `nomic-embed-text-v1.5` model was [trained with Matryoshka learning](https://blog.nomic.ai/posts/nomic-embed-matryoshka)
        # to enable variable-length embeddings with a single model.
        # This means that you can specify the dimensionality of the embeddings at inference time.
        # The model supports dimensionality from 64 to 768.
        # inference_mode="remote",
        # One of `remote`, `local` (Embed4All), or `dynamic` (automatic). Defaults to `remote`.
        # api_key=... , # if using remote inference,
        # device="cpu",
        # The device to use for local embeddings. Choices include
        # `cpu`, `gpu`, `nvidia`, `amd`, or a specific device name. See
        # the docstring for `GPT4All.__init__` for more info. Typically
        # defaults to CPU. Do not use on macOS.
    )
    result['DB'] = FAISS.load_local(result['DB_INDEX_LOCATION'], result['UNDERLYING_EMBEDDINGS'], allow_dangerous_deserialization=True)
    result['RETRIEVER'] = result['DB'].as_retriever()

    return result


def similarity_search(question,db, n):
    """
    similarity_search 

    Example call:

    similarity_search("Who is Gwen Stills?", chrome_db, 3)
    Args:
        question (str): The question the user asked that might be answerable from the searchable documents
        db (FAIS): FAIS object/Database
        b (int): value k for similarity search. 
    Returns:
        str: The list of texts (and their sources) that matched with the question the closest using RAG
    """
    
    similar_docs = db.similarity_search(question, k=n)

    # for doc in similar_docs:
    #     print(doc)               
    docs_formatted = list(map(lambda doc: f"meta: {doc.metadata}\n Content: {doc.page_content}", similar_docs))
    return docs_formatted


CONFIG = init()

result = similarity_search("What is faiss?", CONFIG['DB'],3)
for el in result:
     print(el)

#print(similarity_search("what is a file_wrapper?", CONFIG['DB'],1))
