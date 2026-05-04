from statistics import mode

import streamlit as st
from backend.rag_engine import generate_response_with_sources

def render():
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Actions", key="chat_back"):
            st.session_state.current_view = 'ACTION'
            st.rerun()
            
    st.markdown("### Interactive Q&A")
    st.caption("Ask specific questions against your uploaded documents.")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
   
    # --- Mode Selection ---
    st.markdown("### Choose a Mode")
    mode = st.selectbox(
      "Select what you want to do:",
      ["qpaper", "summary", "flashcard", "eval"],
      format_func=lambda x: {
        "qpaper": "📝 Question Paper",
        "summary": "🧾 Summary",
        "flashcard": "🃏 Flashcards",
        "eval": "🧠 Evaluation"
    }[x]
)
    import config
    config.SELECTED_TOOL = mode
# Store selected mode in session state (used by backend)
    st.session_state.selected_mode = mode

        
    # Display history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    # Chat Input
    if prompt := st.chat_input("Ask a question about the document..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
            
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if st.session_state.rag_chain:
                answer, sources = generate_response_with_sources(
    st.session_state.rag_chain,
    prompt
)

                
                st.markdown(answer)

                # ✅ store assistant reply
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer
                })

                if sources:
                    st.markdown(f"**Sources:** {', '.join(sources)}")
            else:
                st.warning("No active RAG chain found. Please upload documents first.")