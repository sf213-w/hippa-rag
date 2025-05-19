# LLM Manual Q&A Assistant

A local question-answering assistant powered by [LLaMA 3.2 via Ollama] and [LangChain]. This tool allows users to query a manual using natural language, and the model will respond using the manual's content, including citations for the page and chapter where the information was found.

## Project Purpose

This project was developed to analyze and answer questions based on customer survey documentation. Since responses were given in free-text format, a language model approach was necessary to interpret and summarize user feedback effectively.

---

## Features

- Local LLM (no cloud dependencies)
- Supports querying large manuals or documents
- Answers include source citations (page and chapter)
- Efficient retrieval via vector database
- Easily extendable to other documents or manuals

---

## Setup Instructions (Windows PowerShell)

### Prerequisites

- Python 3.8 or higher installed
- [Ollama](https://ollama.com) installed and running locally
- LLaMA model pulled:

```powershell
    ollama pull llama3.2
```

#### Step 1: Open PowerShell and Navigate to the Project Folder

```powershell
    ollama pull llama3.2
```
