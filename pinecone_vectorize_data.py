#!/usr/bin/env python3
"""
VectorizeDataManager - A tool to create vector stores from various file types using Pinecone.

This script allows you to vectorize individual files or entire directories of files,
supporting both text and PDF formats. The vectorized data is stored in a Pinecone
vector store for efficient similarity search and retrieval.

Usage:
    python3 pinecone_vectorize_data.py <input_path> [-o <index_name>] [-e <environment>]
"""

import os
import argparse
from typing import List, Optional
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone
from pinecone import Pinecone, ServerlessSpec

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

def create_vector_store(documents: List[str], index_name: str, environment: str) -> None:
    """
    Create a vector store from the provided documents using Pinecone.
    
    Args:
        documents: List of document texts to vectorize
        index_name: Name of the Pinecone index to use
        environment: Pinecone environment to use
    """
    # Initialize Pinecone
    pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
    
    # Create index if it doesn't exist
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=1536,  # OpenAI embeddings dimension
            metric="cosine",
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(documents)
    
    # Create embeddings and vector store
    embeddings = OpenAIEmbeddings()
    
    # Create vector store and add documents
    vectorstore = Pinecone.from_documents(
        documents=splits,
        embedding=embeddings,
        index_name=index_name
    )

def main():
    parser = argparse.ArgumentParser(description='Vectorize files or directories using Pinecone')
    parser.add_argument('input_path', help='Path to input file or directory')
    parser.add_argument('-o', '--output', help='Name of the Pinecone index', default='vector-store')
    parser.add_argument('-e', '--environment', help='Pinecone environment', default='gcp-starter')
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
        create_vector_store(documents, args.output, args.environment)
        print(f"Successfully vectorized documents from '{args.input_path}'")
        print(f"Vector store created in Pinecone index '{args.output}'")
            
    except Exception as e:
        print(f"Error during vectorization: {str(e)}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
