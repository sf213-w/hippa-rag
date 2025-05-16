# ingest.py
# Step 1: Load the manual, split into chunks, and embed with metadata (chapter/page)

import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma

# Load and parse PDF
loader = PyPDFLoader("manual.pdf")
documents = loader.load()

# Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)

# Embed using Ollama
embedding = OllamaEmbeddings(model="llama3")
vectorstore = Chroma.from_documents(chunks, embedding, persist_directory="vectorstore")

print(f"Ingested and stored {len(chunks)} chunks.")