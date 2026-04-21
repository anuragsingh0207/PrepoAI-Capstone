import streamlit as st
from backend.ingestion import load_documents
from backend.embeddings import get_vector_store
from backend.rag_engine import get_rag_chain

def render():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem; margin-top: 2rem;">
        <h1 style="font-size:28px; font-weight:600; color:#f0ede8;">Upload Material</h1>
        <p style="color:#a8a69f;">Drop your study PDF to begin building your knowledge base.</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Supported formats: PDF, PPTX",
        accept_multiple_files=True,
        type=["pdf", "pptx", "ppt", "txt", "docx"],
        label_visibility="hidden"
    )

    # Mock up instruction section
    st.markdown("""
    <div style="text-align: center; margin-top: 6rem; margin-bottom: 3rem;">
        <h2 style="font-size:26px; font-weight:600; color:#f0ede8;">How PrepoAI Works</h2>
    </div>
    <div style="display: flex; justify-content: space-around; text-align: center; align-items: flex-start; max-width: 800px; margin: 0 auto; padding-bottom:4rem;">
        <div style="flex:1; padding: 0 15px;">
            <div style="font-size: 2.2rem; color: #f0ede8; margin-bottom: 12px; font-weight:300;">↑</div>
            <h4 style="font-size: 15px; font-weight: 700; color:#f0ede8; letter-spacing:0.5px; text-transform:uppercase;">1. UPLOAD</h4>
            <p style="font-size: 13px; color: #a8a69f; margin-top:8px; line-height:1.5;">Upload your study PDF file your compact knowledge base.</p>
        </div>
        <div style="flex:1; padding: 0 15px;">
            <div style="font-size: 2.2rem; color: #f0ede8; margin-bottom: 12px; font-weight:300;">☷</div>
            <h4 style="font-size: 15px; font-weight: 700; color:#f0ede8; letter-spacing:0.5px; text-transform:uppercase;">2. INDEX</h4>
            <p style="font-size: 13px; color: #a8a69f; margin-top:8px; line-height:1.5;">Index the index game ensuring and time evaluation.</p>
        </div>
        <div style="flex:1; padding: 0 15px;">
            <div style="font-size: 2.2rem; color: #f0ede8; margin-bottom: 12px; font-weight:300;">🕮</div>
            <h4 style="font-size: 15px; font-weight: 700; color:#f0ede8; letter-spacing:0.5px; text-transform:uppercase;">3. STUDY</h4>
            <p style="font-size: 13px; color: #a8a69f; margin-top:8px; line-height:1.5;">Study options data barriers to study study and stops.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if uploaded_files:
        if st.button("Start Processing >", type="primary", use_container_width=True):
            with st.spinner("Analyzing your documents and building vectors..."):
                try:
                    docs = load_documents(uploaded_files)
                    if docs:
                        vector_store = get_vector_store(docs)
                        st.session_state.rag_chain = get_rag_chain(vector_store)
                        st.session_state.current_view = 'ACTION'
                        st.rerun()
                    else:
                        st.error("No valid text found in the uploaded documents.")
                except Exception as e:
                    st.error(f"Error processing documents: {e}")
