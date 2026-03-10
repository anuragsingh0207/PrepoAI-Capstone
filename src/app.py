"""
app.py
Responsibility: Anisha

This module contains the Streamlit code for the user interface.
It connects the Ingestion, Embeddings, and RAG Engine modules.
"""
import streamlit as st
import time
from langchain_core.messages import HumanMessage, AIMessage

# Import internal modules
from ingestion import load_documents
from embeddings import get_vector_store
from rag_engine import get_rag_chain

st.set_page_config(page_title="PrepoAI", page_icon="📘")

def main():
    st.title("PrepoAI: Intelligent Educational RAG System")
    st.write("Welcome to your AI Study Companion. Upload your notes (PDF/PPTX) and start a deep conversation or generate exam questions.")

    # Sidebar for File Upload
    with st.sidebar:
        st.header("Your Material")
        uploaded_files = st.file_uploader(
            "Upload lecture notes, slides, or textbooks", 
            type=['pdf', 'pptx', 'ppt'], 
            accept_multiple_files=True
        )
        
        process_btn = st.button("Process Documents")

    # Session State Initialization
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "rag_chain" not in st.session_state:
        st.session_state.rag_chain = None

    # Processing Logic
    if process_btn and uploaded_files:
        with st.spinner("Ingesting and Embedding Documents..."):
            try:
                # 1. Ingest
                docs = load_documents(uploaded_files)
                st.sidebar.success(f"Loaded {len(docs)} chunks from {len(uploaded_files)} files.")
                
                # 2. Embed
                vector_store = get_vector_store(docs)
                st.sidebar.success("Vector Store Created.")
                
                # 3. Initialize Chain
                st.session_state.rag_chain = get_rag_chain(vector_store)
                st.sidebar.success("RAG Engine Ready!")
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

    # Chat Interface
    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)

    # Input Area
    user_input = st.chat_input("Ask a question about your documents...")

    # Logic for interaction
    if user_input:
        handle_user_input(user_input)
    
    # helper button for exam questions (if chain works)
    if st.session_state.rag_chain:
         if st.sidebar.button("Generate Exam Questions"):
             handle_user_input("Generate a comprehensive list of exam questions based on the uploaded documents, following the strict output structure.")


def handle_user_input(input_text):
    if not st.session_state.rag_chain:
        st.error("Please upload and process documents first.")
        return

    # Add user message to UI immediately
    st.chat_message("user").markdown(input_text)
    
    # We append to history here for the UI, but the chain also manages history 
    # via the chat_history arg we pass to it.
    st.session_state.chat_history.append(HumanMessage(content=input_text))

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # The chain expects 'input' and 'chat_history'
                response = st.session_state.rag_chain.invoke({
                    "input": input_text,
                    "chat_history": st.session_state.chat_history
                })
                
                answer = response["answer"]
                st.markdown(answer)
                
                # Append AI response to history
                st.session_state.chat_history.append(AIMessage(content=answer))
                
            except Exception as e:
                st.error(f"Error generating response: {e}")

if __name__ == "__main__":
    main()
