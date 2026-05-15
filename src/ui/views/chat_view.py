import sys, os as _os
_UI_DIR = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), ".."))
if _UI_DIR not in sys.path:
    sys.path.insert(0, _UI_DIR)
import streamlit as st
from styles import page_header_html
from config import get_gemini_client, stream_chat_response, build_context_from_docs
from constants import FOREST, SAND, RUST, SAGE, CREAM, WHITE, PAGE_UPLOAD

def render():
    st.markdown(page_header_html("💬", "AI Chat", "Ask questions about your uploaded study material"), unsafe_allow_html=True)

    docs = st.session_state.get("uploaded_docs", [])
    client = get_gemini_client()

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    #No docs warning 
    if not docs:
        st.markdown(f"""
        <div style="background:{CREAM};border:1.5px solid {SAND}50;border-radius:14px;padding:20px 24px;margin-bottom:16px;text-align:center;">
            <div style="font-size:32px;margin-bottom:10px;">📭</div>
            <div style="font-size:16px;font-weight:600;color:{FOREST};margin-bottom:6px;">No documents loaded</div>
            <div style="font-size:13.5px;color:{SAGE};">Upload your study material first so Prepo AI can answer questions from it.</div>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📄 Go to Upload", use_container_width=True):
                st.session_state["current_page"] = PAGE_UPLOAD
                st.rerun()
        st.info("You can still chat — Prepo AI will use its general knowledge without specific material context.")

    #Context bar
    if docs:
        doc_names = ", ".join(d["name"] for d in docs[:3])
        if len(docs) > 3:
            doc_names += f" +{len(docs)-3} more"
        st.markdown(f"""
        <div style="background:{WHITE};border:1px solid {SAND}28;border-radius:10px;padding:10px 16px;margin-bottom:16px;display:flex;align-items:center;gap:10px;">
            <span style="font-size:16px;">📚</span>
            <div>
                <span style="font-size:12px;font-weight:600;color:{SAGE};text-transform:uppercase;letter-spacing:0.8px;">Context: </span>
                <span style="font-size:13px;color:{FOREST};">{doc_names}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    #Chat controls
    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([1, 1, 4])
    with col_ctrl1:
        if st.button("🗑 Clear Chat"):
            st.session_state.chat_messages = []
            st.rerun()
    with col_ctrl2:
        with st.expander("⚙️ Settings"):
            st.session_state["temperature"] = st.slider("Creativity", 0.0, 1.0, 0.7, 0.1, key="chat_temp")
            st.session_state["max_tokens"] = st.select_slider("Max length", [512, 1024, 2048, 4096], 2048, key="chat_tok")

    #Suggested questions
    if not st.session_state.chat_messages:
        st.markdown(f"""<div style="font-size:13px;font-weight:600;color:{SAGE};text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">Try asking…</div>""", unsafe_allow_html=True)
        suggestions = [
            "Summarize the key topics in my material",
            "What are the most important concepts I should know?",
            "Give me a quick overview of the main subjects",
            "What questions might be asked about this in an interview?",
        ]
        cols = st.columns(2)
        for i, s in enumerate(suggestions):
            with cols[i % 2]:
                if st.button(f"💡 {s}", key=f"chat_sugg_{i}", use_container_width=True):
                    st.session_state["pending_chat"] = s
                    st.rerun()

    #Display messages 
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"], avatar="🌿" if msg["role"] == "assistant" else "👤"):
            st.markdown(msg["content"])

    #Handle pending suggestion 
    if "pending_chat" in st.session_state:
        prompt = st.session_state.pop("pending_chat")
        _process_message(client, docs, prompt)
        st.rerun()

    #Chat input 
    if user_input := st.chat_input("Ask about your material…"):
        _process_message(client, docs, user_input)
        st.rerun()


def _process_message(client, docs, prompt: str):
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    context = build_context_from_docs(docs)

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🌿"):
        with st.spinner(""):
            response = st.write_stream(
                stream_chat_response(client, st.session_state.chat_messages, context)
            )

    st.session_state.chat_messages.append({"role": "assistant", "content": response})
    if "stats" not in st.session_state:
        st.session_state.stats = {}
    st.session_state.stats["questions_answered"] = \
        st.session_state.stats.get("questions_answered", 0) + 1
