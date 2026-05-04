import streamlit as st
from backend.prompts import build_eval_prompt
from backend.rag_engine import generate_response_with_sources

def render():
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Actions", key="eval_back"):
            st.session_state.current_view = 'ACTION'
            st.rerun()

    st.markdown("### 🧠 Evaluation Mode")
    st.caption("Paste a question and your answer to get instant feedback and marks.")

    q = st.text_area("📘 Question", placeholder="Enter the exam question...")
    a = st.text_area("✍️ Your Answer", placeholder="Write your answer here...")
    marks = st.slider("Maximum Marks", 1, 20, 10)

    if st.button("Evaluate", type="primary"):
        if not q or not a:
            st.warning("Please enter both a question and an answer first.")
            return

        prompt = build_eval_prompt(q, a, max_marks=marks)

        with st.spinner("Evaluating..."):
            try:
                answer, sources = generate_response_with_sources(st.session_state.rag_chain, prompt)
                st.markdown("### 🧾 Evaluation Report")
                st.markdown(answer)
                if sources:
                    with st.expander("📚 Sources"):
                        for src in sources:
                            st.markdown(f"- {src}")
            except Exception as e:
                st.error(f"Error: {e}")
