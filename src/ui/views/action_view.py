import streamlit as st

def render():
    # Breadcrumb / Control bar
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Re-upload"):
            st.session_state.rag_chain = None
            st.session_state.current_view = 'UPLOAD'
            st.rerun()

    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="font-size:24px; color:#f0ede8;">Knowledge Base Active</h2>
        <p style="color:#a8a69f;">Documents are processed. What do you want to accomplish today?</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        if st.button("📄 Generate Question Paper", use_container_width=True):
            st.session_state.current_view = 'Q_PAPER'
            st.rerun()
            
    with c2:
        if st.button("⏱️ Start Mock Test", use_container_width=True):
            st.session_state.current_view = 'MOCK_TEST'
            st.rerun()
            
    with c3:
        if st.button("💬 Ask Questions", use_container_width=True):
            st.session_state.current_view = 'ASK_Q'
            st.rerun() 
    st.markdown("<br>", unsafe_allow_html=True)
    # 🧠 Evaluation mode button
    if st.button("🧠 Evaluation Mode", use_container_width=True):
        st.session_state.current_view = "EVAL"
        st.rerun()
