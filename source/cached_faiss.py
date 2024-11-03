from langsmith import traceable

from langchain.storage import LocalFileStore
from langchain_community.document_loaders import TextLoader

from langchain_community.vectorstores import FAISS
from langchain.embeddings import CacheBackedEmbeddings
from langchain_nomic import NomicEmbeddings
from langchain_text_splitters import CharacterTextSplitter

import json

import os

def load_config():
    with open("config.json","r") as f:
        str = f.read()
    CONFIG = json.loads(str)
    return CONFIG


def init():
    result = load_config()
    #result['BASE_URL'] = "127.0.0.1:11434"
    #result['EMBEDDING_MODEL'] = "nomic-embed-text-v1.5"
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
    #result['STORE_LOCATION'] = "./cache/"
    result['STORE'] = LocalFileStore(result['STORE_LOCATION'])
    result['CACHED_EMBEDDER'] = CacheBackedEmbeddings.from_bytes_store(
        result['UNDERLYING_EMBEDDINGS'], result['STORE'], namespace=result['EMBEDDING_MODEL']
    )
    #result['SOURCE_FOLDER'] = "input"
    result['RAW_DOCUMENTS'] = load_all(result['SOURCE_FOLDER'])
    result['TEXT_SPLITTER'] = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    result['RAW_DOCUMENTS'] = result['TEXT_SPLITTER'].split_documents(result['RAW_DOCUMENTS'])
    result['DB'] = FAISS.from_documents(result['RAW_DOCUMENTS'], result['CACHED_EMBEDDER'])
    result['RETRIEVER'] = result['DB'].as_retriever()
    result['DB'].save_local(result['DB_INDEX_LOCATION'])
    return result


def load_all(folder):
    path = os.path.join(folder,"story.txt")
    raw_documents = TextLoader(path).load()
    return raw_documents




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
    docs_formatted = list(map(lambda doc: f"Source: {doc.metadata.get('source', 'NA')}\nContent: {doc.page_content}", similar_docs))
    return str(docs_formatted)


CONFIG = init()

