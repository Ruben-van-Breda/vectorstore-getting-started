python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

pip install langchain-community langchain-openai chromadb

# Chroma DB
1. Create a vectorstore from some files
```
python3 chroma_vectorize_data.py midsummer-nights-dream.txt -o output_directory
```
2. Query the Vectorstore
```
python3 context_agent.py --query "what is the poem about" --directory output_directory
```

3. Similarity Search
```
python3 context_agent.py --query "What are dogs"
```

# For a single file
python3 vectorize_data.py input.txt -o output_directory

# For a directory
python3 vectorize_data.py ./input_directory -o output_directory