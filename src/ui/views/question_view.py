import streamlit as st
from backend.prompts import build_dynamic_prompt
from backend.rag_engine import generate_response

def render():
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Actions"):
            st.session_state.current_view = 'ACTION'
            st.rerun()

    st.markdown("### Generate Question Paper")
    
    with st.container():
        st.markdown('<div class="config-panel-st">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            q_count = st.number_input("Question count", min_value=5, max_value=100, value=20)
        with c2:
            difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard", "Mixed"], index=1)
            
        st.markdown("**Question Types**")
        t1, t2, t3, t4 = st.columns(4)
        with t1:
            mcq = st.checkbox("MCQ", value=True)
        with t2:
            short = st.checkbox("Short Answer", value=True)
        with t3:
            long_ans = st.checkbox("Long Answer", value=False)
        with t4:
            tf = st.checkbox("True / False", value=False)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Generate Paper", type="primary", use_container_width=True):
        config = {
            "q_count": q_count,
            "difficulty": difficulty,
            "qt_mcq": mcq,
            "qt_short": short,
            "qt_long": long_ans,
            "qt_tf": tf
        }
        prompt = build_dynamic_prompt('qpaper', config)
        
        with st.spinner("Forging your question paper..."):
            try:
                response = generate_response(st.session_state.rag_chain, prompt)
                st.session_state.qpaper_result = response["answer"]
            except Exception as e:
                st.error(f"Error: {e}")

    if st.session_state.get('qpaper_result'):
        st.markdown("---")
        st.markdown(st.session_state.qpaper_result)
        
        # In a real app we would cache questions to check answers against, but for now we just show a static placeholder
        if st.button("Generate Answers", use_container_width=True):
            st.info("Answer Generation requested! (Prompt logic here)")
