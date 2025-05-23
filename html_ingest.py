# html_ingest.py
# Load website HTMLs from a URL list file, extract text, split, embed, and store

import argparse
import requests
from bs4 import BeautifulSoup
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import time
import os

def read_urls_from_file(filename):
	with open(filename, "r") as f:
		urls = [line.strip() for line in f if line.strip()]
	return urls

def fetch_html(url):
	try:
		print(f"Fetching: {url}")
		resp = requests.get(url, timeout=10)
		soup = BeautifulSoup(resp.content, "html.parser")
		text = soup.get_text(separator="\n", strip=True)
		return Document(page_content=text, metadata={"source": url})
	except Exception as e:
		print(f"Failed to fetch {url}: {e}")
		return None

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Ingest website HTML content from a list of URLs.")
	parser.add_argument("--url-file", type=str, required=True, help="Path to a text file containing URLs (one per line)")
	args = parser.parse_args()

	# Step 1: Load URLs
	if not os.path.isfile(args.url_file):
		print(f"File not found: {args.url_file}")
		exit(1)

	url_list = read_urls_from_file(args.url_file)

	# Step 2: Download and parse each URL
	raw_docs = []
	for url in url_list:
		doc = fetch_html(url)
		if doc:
			raw_docs.append(doc)
		time.sleep(0.5)  # Politeness delay

	# Step 3: Split into chunks
	splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
	chunks = splitter.split_documents(raw_docs)

	# Step 4: Embed and store
	embedding = OllamaEmbeddings(model="llama3.2")
	vectorstore = Chroma.from_documents(chunks, embedding, persist_directory="vectorstore")

	print(f"Ingested and stored {len(chunks)} chunks from {len(url_list)} URLs.")
