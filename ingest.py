# ingest.py
# Step 1: Load the manual, split into chunks, and embed with metadata (chapter/page)

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# Load and parse PDF
loader = PyPDFLoader("HIPAA_Training_Buyers_Guide_CJ - Final.pdf")
documents = loader.load()

# Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)

# Embed using Ollama
embedding = OllamaEmbeddings(model="llama3.2")
vectorstore = Chroma.from_documents(chunks, embedding, persist_directory="vectorstore")

print(f"Ingested and stored {len(chunks)} chunks.")
