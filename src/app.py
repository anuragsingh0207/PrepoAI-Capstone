
import streamlit as st

try:
    import config
except ImportError:
    pass

from ui.styles import inject_custom_css
from ui.views import upload_view, action_view, question_view, mock_test_view, result_view, chat_view, eval_view


st.set_page_config(page_title="PrepoAI", page_icon="⚒️", layout="wide")

# 1. Inject Styles
inject_custom_css() 

import streamlit as st

try:
    import config
except ImportError:
    pass

from ui.styles import inject_custom_css
from ui.views import upload_view, action_view, question_view, mock_test_view, result_view, chat_view, eval_view


st.set_page_config(page_title="PrepoAI", page_icon="⚒️", layout="wide")

# 1. Inject Styles
inject_custom_css()

# Global Navigation Bar (Matching Mockup)
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center; padding: 15px 40px; margin:-0 -0 2rem -0; border-bottom: 0.5px solid rgba(255,255,255,0.05); background:#141412;">
    <div style="display:flex; align-items:center; gap:8px;">
        <span style="font-size:20px; color:#5DCAA5;">✨</span>
        <span style="font-size:18px; font-weight:700; color:#ffffff; font-family:'Sora',sans-serif; letter-spacing:-0.5px;">Prepo<span style="color:#ffffff;">AI</span><sup style="color:#5DCAA5;">✦</sup></span>
    </div>
    <div style="display:flex; gap:30px; font-family:'Sora',sans-serif; font-size:13px; color:#a8a69f; font-weight:500;">
        <span style="cursor:pointer;">Features</span>
        <span style="cursor:pointer;">How it Works</span>
        <span style="cursor:pointer;">Pricing</span>
        <span style="cursor:pointer;">Blog</span>
    </div>
    <div style="display:flex; align-items:center; gap:20px; font-family:'Sora',sans-serif;">
        <span style="font-size:13px; color:#a8a69f; font-weight:600; cursor:pointer;">Login</span>
        <button style="background:rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.2); color:#fff; border-radius:30px; padding:8px 20px; font-size:13px; font-weight:500; cursor:pointer;">Get Started</button>
    </div>
</div>
""", unsafe_allow_html=True)

# 2. State Initialization
def init_state():
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'UPLOAD'
    if 'rag_chain' not in st.session_state:
        st.session_state.rag_chain = None

init_state()

# 3. Sidebar Context
with st.sidebar:
    st.markdown("### PrepoAI 📚")
    if st.session_state.rag_chain is None:
        st.caption("No document loaded.")
    else:
        st.success("Active Knowledge Base Loaded")
        if st.button("Reset Session", use_container_width=True):
            st.session_state.clear()
            st.rerun()

# 4. View Router
current_view = st.session_state.get('current_view', 'UPLOAD')

# Central constraint container
st.markdown('<div style="max-width: 1100px; margin: 0 auto;">', unsafe_allow_html=True)

if current_view == 'UPLOAD':
   if "upload_rendered" not in st.session_state:
        st.session_state.upload_rendered = True
        upload_view.render()
   else:
        upload_view.render()
    
elif current_view == 'ACTION':
    action_view.render()
    
elif current_view == 'Q_PAPER':
    question_view.render()
    
elif current_view == 'MOCK_TEST':
    mock_test_view.render()
    
elif current_view == 'RESULT':
    result_view.render()
    
elif current_view == 'ASK_Q':
    chat_view.render()

elif current_view == 'EVAL':
    eval_view.render()
   
else:
    st.error("Invalid View State Accessed.")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center; padding: 20px 40px; margin-top:5rem; border-top: 0.5px solid rgba(255,255,255,0.05);">
    <div style="font-family:'Sora',sans-serif; font-size:12px; color:#6e6c66;">
        Copyright © PrepoAI. All rights reserved. <span style="text-decoration:underline; cursor:pointer; color:#a8a69f;">Privacy Policy</span>
    </div>
    <div style="display:flex; gap:15px; color:#6e6c66; font-size:16px;">
        <span>🐦</span> <span>📘</span> <span>👾</span>
    </div>
</div>
""", unsafe_allow_html=True)




# Global Navigation Bar (Matching Mockup)
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center; padding: 15px 40px; margin:0 0 2rem 0; border-bottom: 0.5px solid rgba(255,255,255,0.05); background:#141412;">
    <div style="display:flex; align-items:center; gap:8px;">
        <span style="font-size:20px; color:#5DCAA5;">✨</span>
        <span style="font-size:18px; font-weight:700; color:#ffffff; font-family:'Sora',sans-serif; letter-spacing:-0.5px;">Prepo<span style="color:#ffffff;">AI</span><sup style="color:#5DCAA5;">✦</sup></span>
    </div>
    <div style="display:flex; gap:30px; font-family:'Sora',sans-serif; font-size:13px; color:#a8a69f; font-weight:500;">
        <span style="cursor:pointer;">Features</span>
        <span style="cursor:pointer;">How it Works</span>
        <span style="cursor:pointer;">Pricing</span>
        <span style="cursor:pointer;">Blog</span>
    </div>
    <div style="display:flex; align-items:center; gap:20px; font-family:'Sora',sans-serif;">
        <span style="font-size:13px; color:#a8a69f; font-weight:600; cursor:pointer;">Login</span>
        <button style="background:rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.2); color:#fff; border-radius:30px; padding:8px 20px; font-size:13px; font-weight:500; cursor:pointer;">Get Started</button>
    </div>
</div>
""", unsafe_allow_html=True)

# 2. State Initialization
def init_state():
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'UPLOAD'
    if 'rag_chain' not in st.session_state:
        st.session_state.rag_chain = None

init_state()

# 3. Sidebar Context
with st.sidebar:
    st.markdown("### PrepoAI 📚")
    if st.session_state.rag_chain is None:
        st.caption("No document loaded.")
    else:
        st.success("Active Knowledge Base Loaded")
        if st.button("Reset Session", use_container_width=True):
            st.session_state.clear()
            st.rerun()

# 4. View Router
current_view = st.session_state.get('current_view', 'UPLOAD')

# Central constraint container
st.markdown('<div style="max-width: 900px; margin: 0 auto;">', unsafe_allow_html=True)

if current_view == 'UPLOAD':
    upload_view.render()
    
elif current_view == 'ACTION':
    action_view.render()
    
elif current_view == 'Q_PAPER':
    question_view.render()
    
elif current_view == 'MOCK_TEST':
    mock_test_view.render()
    
elif current_view == 'RESULT':
    result_view.render()
    
elif current_view == 'ASK_Q':
    chat_view.render()

elif current_view == 'EVAL':
    eval_view.render()
   
else:
    st.error("Invalid View State Accessed.")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center; padding: 20px 40px; margin-top:5rem; border-top: 0.5px solid rgba(255,255,255,0.05);">
    <div style="font-family:'Sora',sans-serif; font-size:12px; color:#6e6c66;">
        Copyright © PrepoAI. All rights reserved. <span style="text-decoration:underline; cursor:pointer; color:#a8a69f;">Privacy Policy</span>
    </div>
    <div style="display:flex; gap:15px; color:#6e6c66; font-size:16px;">
        <span>🐦</span> <span>📘</span> <span>👾</span>
    </div>
</div>
""", unsafe_allow_html=True)


