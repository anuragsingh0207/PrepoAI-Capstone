"""
embeddings.py
Responsibility: Anurag

This module handles the generation of vector embeddings from processed text and storing them in a vector database.
"""
import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

def get_vector_store(docs):
    """
    Creates or updates a FAISS vector store from a list of documents.
    """
    embeddings = HuggingFaceEmbeddings(
      model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vector_store = FAISS.from_documents(
        documents=docs,
        embedding=embeddings
    )
    
    return vector_store

if __name__ == "__main__":
    print("This module provides the get_vector_store function using FAISS.")
