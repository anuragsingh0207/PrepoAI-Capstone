"""
styles.py
Responsibility: UI styling
"""
import streamlit as st

def inject_custom_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Hide all default Streamlit chrome ── */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display: none;}

/* ── Root background ── */
.stApp {
    background: #141412 !important;
    font-family: 'Sora', sans-serif !important;
}

/* ── Strip padding from the main block ── */
.block-container {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    max-width: 860px !important;
}

/* ── File uploader restyling ── */
[data-testid="stFileUploader"] {
    background-color: #1a1a1e !important;
    border: 1px dashed rgba(200, 180, 255, 0.4) !important;
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 0 30px rgba(106, 90, 205, 0.15), inset 0 0 20px rgba(106, 90, 205, 0.05);
    transition: all 0.3s ease;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(200, 180, 255, 0.8) !important;
    box-shadow: 0 0 40px rgba(106, 90, 205, 0.25), inset 0 0 30px rgba(106, 90, 205, 0.1);
}
[data-testid="stFileUploader"] label {
    color: #f0ede8 !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 15px !important;
    font-weight: 500 !important;
}
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] span {
    color: #a8a69f !important;
    font-family: 'Sora', sans-serif !important;
}
[data-testid="stFileUploadDropzone"] {
    background: transparent !important;
    border: none !important;
}

/* ── Button base reset ── */
div.stButton > button {
    font-family: 'Sora', sans-serif !important;
    border-radius: 10px !important;
    transition: all 0.15s ease !important;
}

/* ── Generate button ── */
div.stButton > button[data-testid="stBaseButton-primary"] {
    background: #1D9E75 !important;
    color: white !important;
    border: none !important;
    height: 42px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}
div.stButton > button[data-testid="stBaseButton-primary"]:hover {
    background: #0F6E56 !important;
}

/* ── Secondary buttons (settings gear) ── */
div.stButton > button[data-testid="stBaseButton-secondary"] {
    background: #2a2a27 !important;
    border: 0.5px solid rgba(255,255,255,0.1) !important;
    color: #a8a69f !important;
    height: 42px !important;
}
div.stButton > button[data-testid="stBaseButton-secondary"]:hover {
    border-color: rgba(255,255,255,0.28) !important;
}

/* ── Tool card buttons ── */
.tool-btn > div > button {
    background: #1e1e1c !important;
    border: 0.5px solid rgba(255,255,255,0.1) !important;
    color: #f0ede8 !important;
    text-align: left !important;
    padding: 1rem !important;
    min-height: 130px !important;
    border-radius: 12px !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: flex-start !important;
    justify-content: flex-start !important;
    white-space: normal !important;
    line-height: 1.5 !important;
}
.tool-btn > div > button:hover {
    border-color: rgba(255,255,255,0.18) !important;
    transform: translateY(-1px);
}

/* ── Active tool card ── */
.tool-btn.active > div > button {
    border-color: #1D9E75 !important;
    background: rgba(29,158,117,0.06) !important;
}
.tool-btn.active > div > button::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: #1D9E75;
    border-radius: 12px 12px 0 0;
}

/* ── Pill toggle buttons ── */
.pill-btn > div > button {
    border-radius: 6px !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    padding: 4px 10px !important;
    min-height: 0 !important;
    height: auto !important;
    background: #2a2a27 !important;
    border: 0.5px solid rgba(255,255,255,0.1) !important;
    color: #a8a69f !important;
}
.pill-btn.on > div > button {
    background: #E1F5EE !important;
    border-color: #5DCAA5 !important;
    color: #0F6E56 !important;
}

/* ── Text input & Select box styling ── */
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stSelectbox"] label {
    color: #a8a69f !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 12px !important;
    font-weight: 500 !important;
}
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background: #2a2a27 !important;
    border: 0.5px solid rgba(255,255,255,0.1) !important;
    border-radius: 7px !important;
    color: #f0ede8 !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 13px !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: #1D9E75 !important;
    box-shadow: 0 0 0 2.5px rgba(29,158,117,0.15) !important;
}
[data-testid="stSelectbox"] > div > div {
    background: #2a2a27 !important;
    border: 0.5px solid rgba(255,255,255,0.1) !important;
    border-radius: 7px !important;
    color: #f0ede8 !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 13px !important;
}

/* ── Markdown text defaults ── */
.stMarkdown p, .stMarkdown span, .stMarkdown div {
    font-family: 'Sora', sans-serif !important;
}

/* ── Config panel container ── */
.config-panel-st {
    background: #1e1e1c;
    border: 0.5px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1rem;
}

/* ── Success/Error messages ── */
.stSuccess, .stError, .stWarning {
    font-family: 'Sora', sans-serif !important;
    border-radius: 10px !important;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: #1D9E75 !important;
}

</style>
""", unsafe_allow_html=True)
