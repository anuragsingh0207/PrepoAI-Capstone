"""
test_system.py
Integration test for PrepoAI components.
"""
import os
import sys

# Support emojis in windows console
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from langchain_core.documents import Document

# Ensure we can import modules in the same directory
# Ensure we can import modules from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from backend.embeddings import get_vector_store
from backend.rag_engine import get_rag_chain

def test_pipeline():
    print("1. Creating dummy documents...")
    docs = [
        Document(page_content="PrepoAI is an intelligent educational RAG system designed to help students prepare for exams."),
        Document(page_content="The system uses Google Gemini for generation and Cohere for reranking to ensure high accuracy."),
        Document(page_content="Users can upload PDF and PPTX files to get exam questions."),
    ]
    
    print("2. Creating Vector Store...")
    try:
        vector_store = get_vector_store(docs)
        print("   ✅ Vector Store created successfully.")
    except Exception as e:
        print(f"   ❌ Vector Store creation failed: {e}")
        return

    print("3. Initializing RAG Chain...")
    try:
        chain = get_rag_chain(vector_store)
        print("   ✅ RAG Chain initialized.")
    except Exception as e:
        print(f"   ❌ RAG Chain initialization failed: {e}")
        return

    print("4. Testing Query (Invoking Chain)...")
    try:
        # We need to simulate chat history
        response = chain.invoke({
            "input": "What is PrepoAI?",
            "chat_history": []
        })
        print(f"   ✅ Answer received: {response['answer']}")
    except Exception as e:
        print(f"   ❌ Query failed: {e}")

if __name__ == "__main__":
    test_pipeline()
