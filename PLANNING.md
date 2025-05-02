Expand chroma_vectorize_data.py
include functions to test the simlairy search

Steps:
1. Create a function to load a vectorstore given a filepath
def loadVectorstore(filePath)
2. Create a function to take in a query paramater and perform a simloary search and return the top k results

Flow:
python3 chroma_vectorize_data -query "" -vectorstore ./vectorstore_path
