#!/usr/bin/env python3
"""
VectorizeDataManager - A tool to create vector stores from various file types.

This script allows you to vectorize individual files or entire directories of files,
supporting both text and PDF formats. The vectorized data is stored in a ChromaDB
vector store for efficient similarity search and retrieval.

Usage:
    python3 vectorize_data.py <input_path> [-o <output_path>]
"""

import os
import argparse
from typing import List, Optional
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

def load_documents(file_path: str) -> List[str]:
    """
    Load documents from a file or directory.
    
    Args:
        file_path: Path to the file or directory to load
        
    Returns:
        List of document texts
    """
    if os.path.isdir(file_path):
        loader = DirectoryLoader(file_path, glob="**/*.txt")
        documents = loader.load()
    else:
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path)
        documents = loader.load()
    
    return documents

def create_vector_store(documents: List[str], output_path: Optional[str] = None) -> None:
    """
    Create a vector store from the provided documents.
    
    Args:
        documents: List of document texts to vectorize
        output_path: Optional path to save the vector store
    """
    print("Splitting Document in chunks")
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(documents)

    print(" Create embeddings and vector store")

    # Create embeddings and vector store
    embeddings = OpenAIEmbeddings(
        model="text-embedding-ada-002",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=output_path
    )
    
    if output_path:
        vectorstore.persist()

def loadVectorstore(filePath):
    return Chroma(
        persist_directory=filePath,
        embedding_function=OpenAIEmbeddings(
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
    )

def similaritySearch(vectorstore, query):
    return vectorstore.similarity_search(query)

def similaritySearchWithScore(vectorstore, query):
    results = vectorstore.similarity_search_with_score(query)
    for result in results:
        print(result)
    return results


def main():
    ## Usage
    # ```bash
    # python3 chroma_vectorize_data.py <input_path> [-o <output_path>]
    # ```

    # ```bash
    # python3 chroma_vectorize_data.py ./examples/Shakespeare -o ./vectorstore
    # ```

    parser = argparse.ArgumentParser(description='Vectorize files or directories')
    parser.add_argument('input_path', help='Path to input file or directory')
    parser.add_argument('-o', '--output', help='Path to save vector store')
    args = parser.parse_args()
    
    # Validate input path
    if not os.path.exists(args.input_path):
        print(f"Error: Input path '{args.input_path}' does not exist")
        return 1
    
    try:
        # Load documents
        documents = load_documents(args.input_path)
        if not documents:
            print(f"Error: No documents found in '{args.input_path}'")
            return 1
            
        # Create vector store
        create_vector_store(documents, args.output)
        print(f"Successfully vectorized documents from '{args.input_path}'")
        if args.output:
            print(f"Vector store saved to '{args.output}'")
            
    except Exception as e:
        print(f"Error during vectorization: {str(e)}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main()) 