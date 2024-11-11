from langchain_community.vectorstores import FAISS
from langchain_nomic import NomicEmbeddings
import json
from file_wrapper import File_Wrapper
from file_collection import File_Collection

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

CONFIG = init()

def get_db():
    return CONFIG['DB']

def get_retriever():
    return CONFIG['RETRIEVER']

def get_index_manifest():
    data = File_Collection.deserialize(CONFIG['METADATA_MANIFEST'])
    return data

def vectorize(query):
    return CONFIG['UNDERLYING_EMBEDDINGS'].embed_query(query)