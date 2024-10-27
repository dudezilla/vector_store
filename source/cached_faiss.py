#!/usr/bin/env python
# coding: utf-8
#  https://python.langchain.com/docs/how_to/caching_embeddings/
from langsmith import traceable
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain.storage import LocalFileStore
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import DirectoryLoader
#vector retriever tools
from langchain_community.vectorstores import FAISS
from langchain.embeddings import CacheBackedEmbeddings
#from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_nomic import NomicEmbeddings
from langchain.tools.retriever import create_retriever_tool
from langchain_text_splitters import CharacterTextSplitter

#from langgraph.checkpoint.memory import MemorySaver
#from langgraph.prebuilt import create_react_agent
from typing import List
#from langchain_core.tools import tool
from langchain_ollama import ChatOllama
import json
from load_envs import load_env


load_env()
BASE_URL = "127.0.0.1:11434"
EMBEDDING_MODEL = "nomic-embed-text-v1.5"
#underlying_embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
underlying_embeddings = NomicEmbeddings(
    model=EMBEDDING_MODEL,
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

store = LocalFileStore("./cache/")
cached_embedder = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings, store, namespace=EMBEDDING_MODEL
)
source_folder = "input"

list(store.yield_keys())
raw_documents = TextLoader("./input/story.txt").load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(raw_documents)
db = FAISS.from_documents(documents, cached_embedder)
list(store.yield_keys())[:5]
retriever = db.as_retriever()
result = retriever.invoke("Gwen Stills")
print(type(result))
for el in result:
    print(f"{el}\n")



@tool
def query_documents(question):
    """
    Uses RAG to query documents for information to answer a question
    that requires specific context that could be found in documents

    Example call:

    query_documents("Who is Gwen Stills?")
    Args:
        question (str): The question the user asked that might be answerable from the searchable documents
    Returns:
        str: The list of texts (and their sources) that matched with the question the closest using RAG
    """
    similar_docs = db.similarity_search(question, k=3)
    docs_formatted = list(map(lambda doc: f"Source: {doc.metadata.get('source', 'NA')}\nContent: {doc.page_content}", similar_docs))

    return str(docs_formatted)

available_functions = {
    "query_documents": query_documents
}

def get_model():
#    llm = ChatOllama( model="llama3.1", temperature=0, base_url=BASE_URL)
    llm = ChatOllama( model="llama3.1", temperature=0,)
    return llm

llm = get_model()
llm_with_tools = llm.bind_tools([query_documents])


messages = [{
    "role":"user", 
    "content": "Who is Gwen Stills?"
}]





response_message = llm_with_tools.invoke(messages)





print(response_message.tool_calls)


tool_calls = response_message.tool_calls

for tool_call in tool_calls:
    tool_call_id = tool_call['id']
    tool_name = tool_call['name']
    args = tool_call['args']['question']
    if tool_name in available_functions:
        results = available_functions[tool_name](args)
        messages.append({
            "role":"tool", 
            "tool_call_id":tool_call_id, 
            "name": tool_name, 
            "content":results
        })
        model_response_with_function_call = llm_with_tools.invoke(messages)
        print(model_response_with_function_call)
    else: 
        print(f"Error: function {tool_function_name} does not exist")
else: 
    print(response_message.content) 
    

model_response_with_function_call.content
