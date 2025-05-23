# qa_server.py
# Step 2: Load the vector store and answer questions using a custom prompt with citation info

import os
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.schema import Document
from langchain.vectorstores.base import VectorStoreRetriever

# Load custom prompt template from file
def load_prompt_template(path="prompt.txt"):
	with open(path, "r", encoding="utf-8") as f:
		return f.read()

PROMPT_TEMPLATE = load_prompt_template()

# Load vector store and retriever
embedding = OllamaEmbeddings(model="llama3.2")
vectorstore = Chroma(persist_directory="vectorstore", embedding_function=embedding)
retriever: VectorStoreRetriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 5})

# Load model
llm = OllamaLLM(model="llama3.2")

def ask(question):
	# Retrieve relevant documents
	docs: list[Document] = retriever.invoke(question)
	chunks = [doc.page_content for doc in docs]

	# Build final prompt
	context_text = "\n".join(f" - {chunk}" for chunk in chunks)
	full_prompt = PROMPT_TEMPLATE.format(context=context_text, question=question)

	# Generate answer
	response = llm.invoke(full_prompt)

	# Display answer
	print("\nAnswer:\n", response)

	# Display sources
	print("\nSources:")
	for doc in docs:
		metadata = doc.metadata
		print(f"- Page {metadata.get('page', '?')} in {metadata.get('source', 'HIPAA_Training_Buyers_Guide_CJ - Final.pdf')}")

if __name__ == "__main__":
	while True:
		q = input("Ask a question (or type 'exit'): ")
		if q.lower() == "exit":
			break
		ask(q)
