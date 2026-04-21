import streamlit as st
from backend.rag_engine import generate_response

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
                try:
                    response_dict = generate_response(st.session_state.rag_chain, prompt)
                    reply = response_dict["answer"]
                    st.markdown(reply)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"Error formulating response: {e}")
