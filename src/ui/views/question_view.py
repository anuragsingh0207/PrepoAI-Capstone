import sys, os as _os
_UI_DIR = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), ".."))
if _UI_DIR not in sys.path:
    sys.path.insert(0, _UI_DIR)
import streamlit as st
from styles import page_header_html
from config import get_gemini_client, generate_questions, build_context_from_docs
from constants import (FOREST, SAND, RUST, SAGE, CREAM, WHITE,
                       DIFFICULTY_LEVELS, QUESTION_TYPES,
                       DEFAULT_NUM_QUESTIONS, MIN_QUESTIONS, MAX_QUESTIONS,
                       PAGE_UPLOAD, PAGE_MOCK)

def render():
    st.markdown(page_header_html("⚙️", "Configure Test", "Set up your mock test parameters"), unsafe_allow_html=True)

    docs = st.session_state.get("uploaded_docs", [])

    if not docs:
        st.markdown(f"""
        <div style="background:{CREAM};border:1.5px solid {SAND}50;border-radius:14px;padding:24px;text-align:center;">
            <div style="font-size:36px;margin-bottom:10px;">📭</div>
            <div style="font-size:16px;font-weight:600;color:{FOREST};margin-bottom:6px;">No study material found</div>
            <div style="font-size:13.5px;color:{SAGE};">Please upload documents before generating a test.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📄 Upload Material", use_container_width=True):
            st.session_state["current_page"] = PAGE_UPLOAD
            st.rerun()
        return

    st.markdown(f"""
    <div style="background:{WHITE};border:1.5px solid {SAND}28;border-radius:14px;padding:22px 24px;margin-bottom:20px;">
        <div style="font-size:13px;font-weight:600;color:{SAGE};text-transform:uppercase;letter-spacing:1px;margin-bottom:14px;">Test Configuration</div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        num_q = st.slider("Number of Questions", MIN_QUESTIONS, MAX_QUESTIONS, DEFAULT_NUM_QUESTIONS, 1)
        difficulty = st.selectbox("Difficulty", DIFFICULTY_LEVELS, index=1)
    with c2:
        q_type = st.selectbox("Question Type", QUESTION_TYPES)
        doc_choice = st.multiselect(
            "Documents to use",
            [d["name"] for d in docs],
            default=[d["name"] for d in docs],
            help="Select which documents to generate questions from"
        )

    st.markdown("</div>", unsafe_allow_html=True)

    #Preview
    st.markdown(f"""
    <div style="background:{CREAM};border:1px solid {SAND}30;border-radius:10px;padding:14px 18px;margin-bottom:16px;">
        <div style="font-size:13px;color:{SAGE};margin-bottom:4px;">Preview</div>
        <div style="font-size:15px;font-weight:500;color:{FOREST};">
            {num_q} <span style="color:{RUST};">{difficulty}</span> {q_type} questions 
            from <span style="color:{RUST};">{len(doc_choice) if doc_choice else len(docs)}</span> document(s)
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Generate Questions & Start Test", use_container_width=True, type="primary"):
            if not doc_choice:
                st.warning("Please select at least one document.")
                return

            selected_docs = [d for d in docs if d["name"] in doc_choice]
            context = build_context_from_docs(selected_docs)
            client = get_gemini_client()

            with st.spinner(f"Generating {num_q} {difficulty} {q_type} questions…"):
                questions = generate_questions(client, context, num_q, difficulty, q_type)

            if questions:
                st.session_state["mock_questions"]    = questions
                st.session_state["mock_answers"]      = {}
                st.session_state["mock_submitted"]    = False
                st.session_state["mock_config"]       = {
                    "num_q": num_q, "difficulty": difficulty,
                    "q_type": q_type, "docs": doc_choice
                }
                st.success(f"✅ {len(questions)} questions generated!")
                st.session_state["current_page"] = PAGE_MOCK
                st.rerun()
            else:
                st.error("Failed to generate questions. Please try again or check your documents have enough content.")
