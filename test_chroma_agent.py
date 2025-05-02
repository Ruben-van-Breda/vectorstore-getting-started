# test_chroma_agent.py

from chroma_vectorize_data import loadVectorstore, similaritySearch

def test_chroma_agent():
    vectorstore = loadVectorstore("./bricks")
    query = "What is the content about?"
    results = similaritySearch(vectorstore, query)
    for result in results[0]:
        print(result)

if __name__ == "__main__":
    test_chroma_agent()

