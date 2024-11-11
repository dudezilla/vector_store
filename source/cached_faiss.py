#from langsmith import traceable
import faiss
from langchain.storage import LocalFileStore
#from langchain_community.document_loaders import TextLoader

from langchain_community.vectorstores import FAISS
#from langchain.embeddings import CacheBackedEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_nomic import NomicEmbeddings
f#rom langchain_text_splitters import CharacterTextSplitter

import json
#from crawl import crawl
from file_wrapper import File_Wrapper
from file_collection import File_Collection
from langchain_core.documents import Document

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
    #result['CACHED_EMBEDDER'] = CacheBackedEmbeddings.from_bytes_store(
    #    result['UNDERLYING_EMBEDDINGS'], result['STORE'], namespace=result['EMBEDDING_MODEL']
    #)
    #not splitting the documents.
    #result['TEXT_SPLITTER'] = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    #result['SOURCE_FOLDER'] = "input"
    #result['RAW_DOCUMENTS'] = result['TEXT_SPLITTER'].split_documents(result['RAW_DOCUMENTS'])
    #result['DB'] = FAISS.from_documents(result['RAW_DOCUMENTS'], result['CACHED_EMBEDDER'])0
    
    #I HAVE NO IDEA OF WHAT THIS LINE DOES! "I think it populates something that needs to exists similar to : x={}"
    index = faiss.IndexFlatL2(len(result['UNDERLYING_EMBEDDINGS'].embed_query("hello world")))
    result['DB'] = FAISS(
        embedding_function=result['UNDERLYING_EMBEDDINGS'],
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={}
    )
    result['RAW_DOCUMENTS'] = load_all(result['METADATA_MANIFEST'],result['DB'])
    #result['RETRIEVER'] = result['DB'].as_retriever()
    result['DB'].save_local(result['DB_INDEX_LOCATION'])
    return result


def load_all(file_index,vector_store):
    data = File_Collection.deserialize(file_index)
    receipts = []
    for key,list in data.unique_contents().items():
        top =  list['paths'][0] #First path all the documents in list['paths'] are the same.
        with open(top,"r") as f:
            new_docs = [Document(page_content=f.read(), metadata=list, id=key)]
            receipts += vector_store.add_documents(documents=new_docs)
    return receipts

CONFIG = init()

