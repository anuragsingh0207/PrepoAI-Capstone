"""
embeddings.py
Responsibility: Anurag

This module handles the generation of vector embeddings from processed text and storing them in a vector database.
"""
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

def get_vector_store(docs):
    """
    Creates or updates a FAISS vector store from a list of documents.
    """
    # Use the comprehensive embedding model
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    # Create the vector store using FAISS
    # FAISS is a standard, efficient library for similarity search.
    vector_store = FAISS.from_documents(
        documents=docs,
        embedding=embeddings
    )
    
    return vector_store

if __name__ == "__main__":
    print("This module provides the get_vector_store function using FAISS.")
