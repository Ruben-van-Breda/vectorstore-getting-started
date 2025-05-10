#!/usr/bin/env python3
import os
import argparse
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

def load_environment():
    """Load environment variables from .env file."""
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not found in environment variables")

def create_qa_chain(persist_directory: str):
    """
    Create a QA chain using the Chroma vector store.
    
    Args:
        persist_directory (str): Directory where the Chroma vector store is persisted
        
    Returns:
        RetrievalQA: A QA chain ready to answer questions
    """
    # Initialize embeddings and vector store
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
    
    # Create a prompt template
    prompt_template = """Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    
    Context: {context}
    
    Question: {question}
    
    Answer:"""
    
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    
    # Initialize the LLM
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    
    # Create the QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )
    
    return qa_chain

def main():
    parser = argparse.ArgumentParser(description='Query a Chroma vector store with natural language questions')
    parser.add_argument('-q', '--query', required=True, help='The question to ask')
    parser.add_argument('-d', '--directory', default='./output', help='Directory where the Chroma vector store is persisted')
    
    args = parser.parse_args()
    
    try:
        # Load environment variables
        load_environment()
        
        # Create QA chain
        qa_chain = create_qa_chain(args.directory)
        
        # Get answer
        result = qa_chain({"query": args.query})
        
        # Print answer
        # print("\nAnswer:", result["result"])
        print(result["result"])
        
        # Print source documents if available
        # if result.get("source_documents"):
        #     print("\nSources:")
        #     for i, doc in enumerate(result["source_documents"], 1):
        #         # print(f"{i}. {doc.page_content[:200]}...")
        #         # print(f"{i}. {doc.page_content}")
                
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
