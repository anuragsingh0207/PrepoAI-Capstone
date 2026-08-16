import sys, os

_HERE = os.path.abspath(os.path.dirname(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

_VIEWS = os.path.join(_HERE, "ui", "views")
if _VIEWS not in sys.path:
    sys.path.insert(0, _VIEWS)

_COMPONENTS = os.path.join(_HERE, "ui", "components")
if _COMPONENTS not in sys.path:
    sys.path.insert(0, _COMPONENTS)

import streamlit as st
import importlib

# Page config (must be first Streamlit call)
st.set_page_config(
    page_title="PrepAI — Intelligent Document Workspace",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from styles import get_global_css

# Inject global CSS (hides native sidebar, applies styles)
st.markdown(get_global_css(), unsafe_allow_html=True)

# Session state defaults for decoupled architecture
defaults = {
    "app_mode":            "upload",     # 'upload' | 'workspace'
    "active_document_id": None,          # currently selected doc ID
    "uploaded_docs":      {},            # {doc_id: doc_metadata}
    "workspace_view":     "overview",   # 'overview'|'chat'|'summary'|'mock_test'
    "chat_messages":      {},            # {doc_id: [messages]}
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def _load_module(module_name: str, pkg: str):
    """Dynamically load UI modules to pick up changes"""
    for candidate in (module_name, f"{pkg}.{module_name}"):
        try:
            mod = importlib.import_module(candidate)
            importlib.reload(mod)
            return mod
        except ModuleNotFoundError:
            continue
    raise ImportError(f"Cannot find module '{module_name}'.")

# ---------------------------------------------------------
# Routing Logic
# ---------------------------------------------------------

if st.session_state.app_mode == "upload":
    # The smart empty state gateway
    upload_view = _load_module("upload_view", "views")
    upload_view.render()

elif st.session_state.app_mode == "workspace":
    # The Document Workspace
    # Use a custom column layout for the in-app navigation rail
    col_nav, col_main = st.columns([1.1, 4.5], gap="large")
    
    with col_nav:
        sidebar = _load_module("sidebar", "components")
        sidebar.render()
        
    with col_main:
        workspace_view = _load_module("workspace_view", "views")
        workspace_view.render()