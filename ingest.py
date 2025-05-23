# ingest.py
# Step 1: Load the manuals, split into chunks, and embed with metadata (chapter/page)

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# List of PDF files to load
pdf_files = [
    "HIPAA_Training_Buyers_Guide_CJ - Final.pdf"
    # "hipaa-simplification-201303.pdf",
    # "privacy-and-security-guide.pdf"
]

# Initialize an empty list to store all documents
all_documents = []

# Load and parse each PDF
for file in pdf_files:
    loader = PyPDFLoader(file)
    documents = loader.load()
    all_documents.extend(documents)

# Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(all_documents)

# Embed using Ollama
embedding = OllamaEmbeddings(model="llama3.2")
vectorstore = Chroma.from_documents(chunks, embedding, persist_directory="vectorstore")

print(f"Ingested and stored {len(chunks)} chunks.")