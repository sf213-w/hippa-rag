# qa_server.py
# Step 2: Load the vector store and answer questions with citation info

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.chains import RetrievalQA

# Load vector store and retriever
embedding = OllamaEmbeddings(model="llama3.2")
vectorstore = Chroma(persist_directory="vectorstore", embedding_function=embedding)
retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 5})

# Load model
llm = OllamaLLM(model="llama3.2")
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)

def ask(question):
	response = qa_chain.invoke({"query": question})
	print("Answer:", response["result"])
	print("\nSources:")
	for doc in response["source_documents"]:
		metadata = doc.metadata
		print(f"- Page {metadata.get('page', '?')} in {metadata.get('source', 'HIPAA_Training_Buyers_Guide_CJ - Final.pdf')}")

if __name__ == "__main__":
	while True:
		q = input("Ask a question (or type 'exit'): ")
		if q.lower() == "exit":
			break
		ask(q)
