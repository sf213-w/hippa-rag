# qa_server.py
# Step 2: Load the vector store and answer questions with citation info

from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import Ollama

# Load vector store and retriever
embedding = OllamaEmbeddings(model="llama3")
vectorstore = Chroma(persist_directory="vectorstore", embedding_function=embedding)
retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 5})

# Load model
llm = Ollama(model="llama3")
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)

def ask(question):
	response = qa_chain({"query": question})
	print("Answer:", response["result"])
	print("\nSources:")
	for doc in response["source_documents"]:
		metadata = doc.metadata
		print(f"- Page {metadata.get('page', '?')} in {metadata.get('source', 'manual.pdf')}")

if __name__ == "__main__":
	while True:
		q = input("Ask a question (or type 'exit'): ")
		if q.lower() == "exit":
			break
		ask(q)
