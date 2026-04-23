import sys, os

_HERE = os.path.abspath(os.path.dirname(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

# Also add the views sub-package explicitly
_VIEWS = os.path.join(_HERE, "views")
if _VIEWS not in sys.path:
    sys.path.insert(0, _VIEWS)

import streamlit as st

# Page config (must be first Streamlit call) 
st.set_page_config(
    page_title="Prepo AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

from styles import get_global_css, sidebar_logo_html
from constants import (
    PAGE_HOME, PAGE_UPLOAD, PAGE_CHAT, PAGE_MOCK, PAGE_RESULT, PAGE_ABOUT, ALL_PAGES,
    FOREST, SAND, RUST, SAGE, CREAM, WHITE
)

#Inject global CSS
st.markdown(get_global_css(), unsafe_allow_html=True)

#Session state defaults
defaults = {
    "current_page":    PAGE_HOME,
    "uploaded_docs":   [],
    "chat_messages":   [],
    "mock_questions":  [],
    "mock_answers":    {},
    "mock_submitted":  False,
    "mock_config":     {},
    "test_results":    None,
    "stats":           {"tests_taken": 0, "questions_answered": 0, "avg_score": 0, "all_scores": []},
    "temperature":     0.7,
    "max_tokens":      2048,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


#SIDEBAR
with st.sidebar:
    st.markdown(sidebar_logo_html(), unsafe_allow_html=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    #Navigation
    nav_icons = {
        PAGE_HOME:   "🏠",
        PAGE_UPLOAD: "📄",
        PAGE_CHAT:   "💬",
        PAGE_MOCK:   "🎯",
        PAGE_RESULT: "📊",
        PAGE_ABOUT:  "ℹ️",
    }
    nav_labels = {
        PAGE_HOME:   "Home",
        PAGE_UPLOAD: "Upload Material",
        PAGE_CHAT:   "AI Chat",
        PAGE_MOCK:   "Mock Test",
        PAGE_RESULT: "Results",
        PAGE_ABOUT:  "About",
    }

    for page in ALL_PAGES:
        active = st.session_state.current_page == page
        icon   = nav_icons[page]
        label  = nav_labels[page]

        # Badge for certain pages
        badge = ""
        if page == PAGE_UPLOAD and st.session_state.uploaded_docs:
            badge = f"  [{len(st.session_state.uploaded_docs)}]"
        elif page == PAGE_CHAT and st.session_state.chat_messages:
            badge = f"  [{len(st.session_state.chat_messages)//2}]"
        elif page == PAGE_RESULT and st.session_state.test_results:
            pct = st.session_state.test_results.get("percentage", 0)
            badge = f"  [{pct:.0f}%]"

        btn_label = f"{icon}  {label}{badge}"

        # Style active differently
        if active:
            st.markdown(f"""
            <div style="padding:9px 14px;background:linear-gradient(135deg,{SAND}28,{RUST}15);border:1px solid {SAND}60;border-radius:9px;margin-bottom:4px;color:{CREAM};font-size:13.5px;font-weight:600;">
                {icon}  {label}{badge}
            </div>
            """, unsafe_allow_html=True)
        else:
            if st.button(btn_label, key=f"nav_{page}", use_container_width=True):
                st.session_state.current_page = page
                st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    #Docs status
    docs = st.session_state.uploaded_docs
    if docs:
        st.markdown(f"""
        <div style="padding:10px 12px;background:#FFFFFF0C;border-radius:9px;border:1px solid #FFFFFF15;margin-bottom:8px;">
            <div style="font-size:10px;text-transform:uppercase;letter-spacing:1.2px;color:#FFFFFF50;margin-bottom:5px;">Study Material</div>
            {"".join(f'<div style="font-size:12.5px;color:#FFFFFFB0;padding:2px 0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">📄 {d["name"][:28]}{"…" if len(d["name"])>28 else ""}</div>' for d in docs[:4])}
            {"" if len(docs) <= 4 else f'<div style="font-size:11px;color:#FFFFFF50;margin-top:3px;">+{len(docs)-4} more</div>'}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="padding:10px 12px;background:#FFFFFF08;border-radius:9px;border:1px dashed #FFFFFF20;margin-bottom:8px;text-align:center;">
            <div style="font-size:12px;color:#FFFFFF40;font-style:italic;">No documents loaded</div>
        </div>
        """, unsafe_allow_html=True)

    #Quick stats
    stats = st.session_state.stats
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div style="text-align:center;padding:8px;background:#FFFFFF0C;border-radius:8px;border:1px solid #FFFFFF12;">
            <div style="font-size:18px;font-weight:700;color:{SAND};">{stats.get('tests_taken',0)}</div>
            <div style="font-size:10px;color:#FFFFFF50;text-transform:uppercase;letter-spacing:0.8px;">Tests</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        avg = stats.get('avg_score', 0)
        st.markdown(f"""<div style="text-align:center;padding:8px;background:#FFFFFF0C;border-radius:8px;border:1px solid #FFFFFF12;">
            <div style="font-size:18px;font-weight:700;color:{SAND};">{avg:.0f}%</div>
            <div style="font-size:10px;color:#FFFFFF50;text-transform:uppercase;letter-spacing:0.8px;">Avg Score</div>
        </div>""", unsafe_allow_html=True)

    #Footer
    st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="position:absolute;bottom:0;left:0;right:0;padding:12px 16px;border-top:1px solid #FFFFFF12;background:{FOREST};">
        <div style="display:flex;align-items:center;gap:9px;">
            <div style="width:30px;height:30px;background:linear-gradient(135deg,{SAGE},{FOREST});border-radius:50%;border:2px solid #FFFFFF20;display:flex;align-items:center;justify-content:center;color:{CREAM};font-size:12px;font-weight:600;flex-shrink:0;">P</div>
            <div>
                <div style="font-size:12.5px;font-weight:500;color:{CREAM};">Prepo User</div>
                <div style="font-size:10px;color:{SAND};">✦ Powered by Gemini 2.0</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

#ROUTER
import importlib

def _load_view(module_name: str):
    """Load a view module by name, searching _VIEWS then _HERE."""
    # Try plain name first (works when _VIEWS is on sys.path)
    for candidate in (module_name, f"views.{module_name}"):
        try:
            mod = importlib.import_module(candidate)
            importlib.reload(mod)   # pick up any edits during dev
            return mod
        except ModuleNotFoundError:
            continue
    raise ImportError(f"Cannot find view module '{module_name}'. sys.path={sys.path}")

page = st.session_state.current_page

if page == PAGE_HOME:
    _load_view("action_view").render()

elif page == PAGE_UPLOAD:
    _load_view("upload_view").render()

elif page == PAGE_CHAT:
    _load_view("chat_view").render()

elif page == PAGE_MOCK:
    questions = st.session_state.get("mock_questions", [])
    submitted = st.session_state.get("mock_submitted", False)
    if not questions or submitted:
        _load_view("question_view").render()
    else:
        _load_view("mock_test_view").render()

elif page == PAGE_RESULT:
    _load_view("result_view").render()

elif page == PAGE_ABOUT:
    from styles import page_header_html
    st.markdown(page_header_html("ℹ️", "About Prepo AI"), unsafe_allow_html=True)
    st.markdown(f"""
    <div style="max-width:650px;margin:0 auto;">
        <div style="background:{WHITE};border:1.5px solid {SAND}28;border-radius:14px;padding:28px;margin-bottom:16px;">
            <div style="font-family:'Playfair Display',serif;font-size:26px;font-weight:700;color:{FOREST};margin-bottom:10px;">
                Prepo<span style="color:{RUST};">AI</span>
            </div>
            <p style="font-size:14.5px;color:{SAGE};line-height:1.7;margin-bottom:14px;">
                Prepo AI is an intelligent RAG System for Automated Knowledge Extraction and Adaptive Assessment
                It helps you understand your study material, generate practice questions,
                and evaluate your answers with detailed feedback.
            </p>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:16px;">
                <div style="padding:12px;background:{CREAM};border-radius:10px;border:1px solid {SAND}25;">
                    <div style="font-weight:600;color:{FOREST};margin-bottom:4px;">🤖 AI Engine</div>
                    <div style="font-size:13px;color:{SAGE};">Google Gemini</div>
                </div>
                <div style="padding:12px;background:{CREAM};border-radius:10px;border:1px solid {SAND}25;">
                    <div style="font-weight:600;color:{FOREST};margin-bottom:4px;">🖥️ Framework</div>
                    <div style="font-size:13px;color:{SAGE};">Streamlit</div>
                </div>
                <div style="padding:12px;background:{CREAM};border-radius:10px;border:1px solid {SAND}25;">
                    <div style="font-weight:600;color:{FOREST};margin-bottom:4px;">📄 Supported Files</div>
                    <div style="font-size:13px;color:{SAGE};">PDF, DOCX, TXT, MD</div>
                </div>
                <div style="padding:12px;background:{CREAM};border-radius:10px;border:1px solid {SAND}25;">
                    <div style="font-weight:600;color:{FOREST};margin-bottom:4px;">🏫 Project Type</div>
                    <div style="font-size:13px;color:{SAGE};">Academic</div>
                </div>
            </div>
        </div>
        <div style="background:{CREAM};border:1px solid {SAND}30;border-radius:12px;padding:18px;text-align:center;">
            <div style="font-size:13px;color:{SAGE};">PrepoAI</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
