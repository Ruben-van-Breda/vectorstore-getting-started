# test_chroma_agent.py

import logging
# Configure logging to suppress Chroma's verbose output
logging.getLogger('chromadb').setLevel(logging.WARNING)
logging.getLogger('langchain').setLevel(logging.WARNING)

from chroma_vectorize_data import loadVectorstore, similaritySearch

def test_chroma_agent():
    vectorstore = loadVectorstore("./shakespeare_output")
    query = "How many plays have the actor KING of France"
    results = similaritySearch(vectorstore, query)
    print("\n\nResults from VectorStore: Similarity Search of the query: ", query, "\n------------------\n\n")
    for result in results:
        print(result, "\n")

if __name__ == "__main__":
    test_chroma_agent()

# # Run
# ```bash
# python3 run_agent.py
# ```