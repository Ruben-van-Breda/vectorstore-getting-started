# Willam Shakespeare Poem

Lets create a custom vector store using ChromaDB for a collection of Shakespeares poems.
Dataset: https://github.com/cobanov/shakespeare-dataset/tree/main


# Create VectorStore
```bash
python3 chroma_vectorize_data.py examples/Shakespeare/input_data/shakespeare-dataset-main/text -o ./shakespeare_output
```
# Run Query
```bash
python3 chroma_vectorize_data.py --query "How many poems are there" --directory ./shakespeare_output
```
# Issues
```
pip install unstructured
```