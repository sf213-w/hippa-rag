# html_ingest.py
# Step 1: Load website HTML, extract text, split into chunks, embed, and store with metadata

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import time

# Set the base URL to crawl
BASE_URL = "https://www.hipaajournal.com/effects-of-poor-communication-in-healthcare/"
MAX_PAGES = 10

def is_internal_link(href, domain):
	if not href:
		return False
	parsed = urlparse(href)
	return parsed.netloc == "" or parsed.netloc == domain

def crawl_site(base_url, max_pages=10):
	visited = set()
	to_visit = [base_url]
	text_documents = []

	domain = urlparse(base_url).netloc

	while to_visit and len(visited) < max_pages:
		url = to_visit.pop(0)
		if url in visited:
			continue
		try:
			print(f"Fetching: {url}")
			resp = requests.get(url, timeout=10)
			soup = BeautifulSoup(resp.content, "html.parser")
			text = soup.get_text(separator="\n", strip=True)
			doc = Document(page_content=text, metadata={"source": url})
			text_documents.append(doc)
			visited.add(url)

			# Collect internal links
			for link in soup.find_all("a", href=True):
				href = link["href"]
				full_url = urljoin(url, href)
				if is_internal_link(href, domain) and full_url not in visited:
					to_visit.append(full_url)

			time.sleep(0.5)  # Be polite to servers

		except Exception as e:
			print(f"Failed to fetch {url}: {e}")
	return text_documents

# Step 2: Fetch and process HTML
raw_docs = crawl_site(BASE_URL, MAX_PAGES)

# Step 3: Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(raw_docs)

# Step 4: Embed and store in vectorstore
embedding = OllamaEmbeddings(model="llama3.2")
vectorstore = Chroma.from_documents(chunks, embedding, persist_directory="vectorstore")

print(f"Ingested and stored {len(chunks)} chunks from HTML.")
