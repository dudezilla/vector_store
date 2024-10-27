from langchain_ollama import ChatOllama




BASE_URL = "172.17.0.1:11434"
def get_model():
    llm = ChatOllama( model="llama3.1", temperature=0, base_url=BASE_URL)
    return llm

llm = get_model()





response_message = llm.invoke("What's going on?")


