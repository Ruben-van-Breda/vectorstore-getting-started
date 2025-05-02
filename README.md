# vectorstore-getting-started
Basic python scripts to vectorize data


# Environment Setup
```
source venv/bin/activate
```
# API Keys
```bash
export OPENAI_API_KEY=''
```
# Create python3 environment
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install requirements.txt
```

## Note on LangChain Imports
This project now uses the new `langchain_community` and `langchain_openai` packages for document loaders, vector stores, and embeddings. Ensure you have these installed (see `requirements.txt`).

- Use `from langchain_community.document_loaders import ...` for loaders
- Use `from langchain_community.vectorstores import ...` for vector stores
- Use `from langchain_openai import OpenAIEmbeddings` for OpenAI embeddings
