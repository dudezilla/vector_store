from load_store import get_db

from langchain_community.vectorstores import FAISS
from file_wrapper import File_Wrapper
from file_collection import File_Collection
from load_store import get_db, get_retriever, get_index_manifest, vectorize

document_cache = get_index_manifest()

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

##This feature will need to embed metadata
# #NotImplementedError: FAISS does not yet support get_by_ids
# def get_by_id(id, db):
#     return db.get_by_ids([id])[0]



# def lookup_el(hash, file_locatioins):
#     print(f"hash: {hash} references {len(file_locatioins)} paths on disk.")
#     for file in file_locatioins:
#         #print(type(file))
#         #print(file)
#         #wrapper = document_cache.__getitem__(file)
#         #print(file.to_dict())
#         get_by_id(file.checksum, get_db())

# #document_cache.visit_unique_keys(lookup_el)

def score_result(stra,strb,score):
    result = "NOT THE SAME"
    #print(f"stra: {stra}, strb: {strb}")
    if stra == strb:
        result = "SAME"
    print(f"RESULT: {result} SCORE is: {score}")


def scored_search(q,k,db, callback):
    vector = vectorize(q)
    result = db.similarity_search_with_score_by_vector(vector,k)
    for el in result:
        doc, score = el
        callback(doc.page_content,q, score)
    return result


def search(q, callback):
    return scored_search(q, document_cache.len_files(), get_db(),callback)

def drive_search(q):
    #result = search(q,score_result)
    for el in originals:
        search(el,score_result)


def load_originals(document_collection):
    receipts = []
    #visit unique and load...
    for key,list in document_collection.unique_contents().items():
        top =  list['paths'][0] #First path all the documents in list['paths'] are the same.
        with open(top,"r") as f:
            receipts.append(f.read())
    return receipts

originals = load_originals(document_cache)
drive_search("FAISS")



