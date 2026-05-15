import sys, os as _os
_UI_DIR = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), ".."))
if _UI_DIR not in sys.path:
    sys.path.insert(0, _UI_DIR)
import streamlit as st
from styles import page_header_html, metric_html
from constants import FOREST, SAND, RUST, SAGE, CREAM, WHITE, PAGE_UPLOAD, PAGE_CHAT, PAGE_MOCK, PAGE_RESULT

def render():
    st.markdown(page_header_html("🏠", "Home", "Welcome to your interview prep workspace"), unsafe_allow_html=True)

    #Welcome banner 
    docs_ready = bool(st.session_state.get("uploaded_docs"))
    doc_count  = len(st.session_state.get("uploaded_docs", []))

    if docs_ready:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{SAGE}18,{CREAM});border:1.5px solid {SAGE}40;border-radius:14px;padding:22px 24px;margin-bottom:20px;">
            <div style="font-size:13px;color:{SAGE};font-weight:600;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">✅ Ready to practice</div>
            <div style="font-family:'Playfair Display',serif;font-size:24px;font-weight:700;color:{FOREST};">
                {doc_count} document{"s" if doc_count > 1 else ""} loaded
            </div>
            <div style="font-size:14px;color:{SAGE};margin-top:6px;">Your study material is processed. Start a chat or take a mock test.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{SAND}18,{CREAM});border:1.5px solid {SAND}40;border-radius:14px;padding:22px 24px;margin-bottom:20px;">
            <div style="font-size:13px;color:{RUST};font-weight:600;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">🌿 Get started</div>
            <div style="font-family:'Playfair Display',serif;font-size:24px;font-weight:700;color:{FOREST};">
                Welcome to <span style="color:{RUST};">Prepo AI</span>
            </div>
            <div style="font-size:14px;color:{SAGE};margin-top:6px;">Upload your study material to unlock AI-powered questions and mock tests.</div>
        </div>
        """, unsafe_allow_html=True)

    #Quick actions 
    st.markdown(f"<div style='font-size:13px;font-weight:600;color:{SAGE};text-transform:uppercase;letter-spacing:1px;margin-bottom:12px;'>Quick Actions</div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    actions = [
        (c1, "📄", "Upload Material", "Add PDFs, notes & docs", PAGE_UPLOAD),
        (c2, "💬", "AI Chat", "Ask questions about your material", PAGE_CHAT),
        (c3, "🎯", "Mock Test", "Test your knowledge", PAGE_MOCK),
        (c4, "📊", "View Results", "See your performance", PAGE_RESULT),
    ]
    for col, icon, title, desc, page in actions:
        with col:
            st.markdown(f"""
            <div style="background:{WHITE};border:1.5px solid {SAND}28;border-radius:13px;padding:18px 14px;text-align:center;transition:all 0.2s;margin-bottom:4px;">
                <div style="font-size:28px;margin-bottom:8px;">{icon}</div>
                <div style="font-size:14px;font-weight:600;color:{FOREST};margin-bottom:4px;">{title}</div>
                <div style="font-size:12px;color:{SAGE};line-height:1.4;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Open →", key=f"action_{title}"):
                st.session_state["current_page"] = page
                st.rerun()

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    #Stats row 
    st.markdown(f"<div style='font-size:13px;font-weight:600;color:{SAGE};text-transform:uppercase;letter-spacing:1px;margin-bottom:12px;'>Your Progress</div>", unsafe_allow_html=True)

    s1, s2, s3, s4 = st.columns(4)
    stats = st.session_state.get("stats", {})
    metrics = [
        (s1, str(doc_count), "Documents"),
        (s2, str(stats.get("tests_taken", 0)), "Tests Taken"),
        (s3, str(stats.get("questions_answered", 0)), "Questions"),
        (s4, f"{stats.get('avg_score', 0):.0f}%", "Avg Score"),
    ]
    for col, val, label in metrics:
        with col:
            st.markdown(metric_html(val, label), unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    #How it works
    with st.expander("ℹ️  How Prepo AI works", expanded=not docs_ready):
        st.markdown(f"""
<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;padding:4px 0;">
    <div style="padding:14px;background:{CREAM};border-radius:10px;border:1px solid {SAND}25;">
        <div style="font-size:20px;margin-bottom:6px;">1️⃣</div>
        <div style="font-weight:600;color:{FOREST};margin-bottom:4px;">Upload Your Material</div>
        <div style="font-size:13px;color:{SAGE};">Upload PDFs, Word docs, or paste text. Prepo AI reads and indexes your content.</div>
    </div>
    <div style="padding:14px;background:{CREAM};border-radius:10px;border:1px solid {SAND}25;">
        <div style="font-size:20px;margin-bottom:6px;">2️⃣</div>
        <div style="font-weight:600;color:{FOREST};margin-bottom:4px;">Chat with Your Notes</div>
        <div style="font-size:13px;color:{SAGE};">Ask anything about your material. Prepo AI answers using only your documents.</div>
    </div>
    <div style="padding:14px;background:{CREAM};border-radius:10px;border:1px solid {SAND}25;">
        <div style="font-size:20px;margin-bottom:6px;">3️⃣</div>
        <div style="font-weight:600;color:{FOREST};margin-bottom:4px;">Take a Mock Test</div>
        <div style="font-size:13px;color:{SAGE};">Generate MCQ, short answer, or mixed questions from your material.</div>
    </div>
    <div style="padding:14px;background:{CREAM};border-radius:10px;border:1px solid {SAND}25;">
        <div style="font-size:20px;margin-bottom:6px;">4️⃣</div>
        <div style="font-weight:600;color:{FOREST};margin-bottom:4px;">Review Results</div>
        <div style="font-size:13px;color:{SAGE};">Get detailed feedback, scores, and identify topics you need to revisit.</div>
    </div>
</div>
        """, unsafe_allow_html=True)
