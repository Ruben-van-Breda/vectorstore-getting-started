# test_chroma_agent.py

import logging
# Configure logging to suppress Chroma's verbose output
logging.getLogger('chromadb').setLevel(logging.WARNING)
logging.getLogger('langchain').setLevel(logging.WARNING)

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from chroma_vectorize_data import loadVectorstore, similaritySearch, load_documents, create_vector_store

def test_chroma_agent():
    vectorstore = loadVectorstore("../Shakespeare/shakespeare_output")
    query = "How many plays have the actor KING of France"
    results = similaritySearch(vectorstore, query)
    print("\n\nResults from VectorStore: Similarity Search of the query: ", query, "\n------------------\n\n")
    for result in results:
        print(result, "\n")

def create_dataset(dir):
    # Create datastore for SciFi movies
     # Load documents
    
    documents = load_documents(dir)
    print(documents.__len__())
    # for doc in documents:
        # print(doc)


if __name__ == "__main__":
    documents = load_documents('./input_data/internet_archive_scifi_v3.txt')

    # Create vector store
    # create_vector_store(documents, './output_data')
    
    # Query Data
    vectorstore = loadVectorstore("./output_data")
    query = "What is the content about?"
    results = similaritySearch(vectorstore, query)
    print(results)
    # test_chroma_agent()

# # Run
# ```bash
# python3 run_agent.py
# ```