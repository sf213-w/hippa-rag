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

## Setup Instructions

### Prerequisites

- Python 3.8 or higher installed
- [Ollama](https://ollama.com) installed and running locally
- LLaMA model pulled:

```bash
    ollama pull llama3.2
```

#### Step 1: Open a Terminal and Navigate to the Project Folder

```bash
    cd path/to/your/project
```

#### Step 2: Create a Virtual Environment

```bash
    python -m venv venv
```

#### Step 3: Activate the Environment

For Windows PowerShell

```bash
    .\venv\Scripts\Activate
```

If attempting to activate the virtual enviornment provides an error message saying running scripts is disabled on this system then you may need to change the exectution policy.
Run the following command to change the excecution policy for the current PowerShell session.

```bash
    Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

#### Step 4: Install Requirements

This repository contains requirements.txt, a text file containing the names of the packages this requires.
Run the following command to install the packages while in the virtual enviornment.

```bash
    pip install -r requirements.txt
```

#### Step 5: Run the Scripts

Load your manual into the vector database:

```bash
    python ingest.py
```

Run the qa_server script (Reword)

```bash
    python qa_server.py
```

Ask a question.
