"""
sidebar.py — Premium sidebar matching the reference design.

Layout (top → bottom):
  ① PrepAI logo + WORKSPACE label
  ② Upload New File CTA button
  ③ RECENT DOCUMENTS section  ← doc list with active highlight
  ④ View all documents →
  ⑤ TOOLS section (Overview, Contextual Chat, AI Playground [Soon])
  ⑥ AI Ready status card (pinned to bottom)
"""
import time
import streamlit as st
from constants import SAGE, FOREST, CREAM, SAND, RUST, WHITE


def render():
    # ── Brand logo ──────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="margin-bottom:28px;">
        <div style="font-family:'Playfair Display',serif;font-size:22px;font-weight:700;
                    color:{FOREST};line-height:1.1;">
            Prep<span style="color:{RUST};">AI</span>
        </div>
        <div style="font-size:9.5px;color:#9E9B96;letter-spacing:1.8px;
                    text-transform:uppercase;margin-top:2px;">Workspace</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Upload New File ──────────────────────────────────────────────────────
    if st.button("＋  Upload New File", use_container_width=True, type="primary"):
        st.session_state.app_mode = "upload"
        st.rerun()

    # ── RECENT DOCUMENTS ────────────────────────────────────────────────────
    st.markdown(
        '<div class="section-label" style="margin-top:24px;">Recent Documents</div>',
        unsafe_allow_html=True
    )

    docs       = st.session_state.get("uploaded_docs", {})
    active_id  = st.session_state.get("active_document_id")

    if not docs:
        st.markdown(
            f'<div style="font-size:12.5px;color:#B0ADA6;padding:4px 0;">No documents yet.</div>',
            unsafe_allow_html=True
        )
    else:
        for doc_id, doc_meta in list(docs.items())[:6]:   # max 6 in sidebar
            name      = doc_meta.get("name", "Document")
            is_active = (doc_id == active_id)
            short     = name[:22] + "…" if len(name) > 22 else name
            label     = f"📄  {short}"

            if is_active:
                st.markdown(f"""
                <div style="background:{FOREST};color:{CREAM};border-radius:9px;
                            padding:9px 12px;font-size:13px;font-weight:600;
                            margin-bottom:4px;cursor:default;
                            border:1.5px solid {FOREST};">
                    {label}
                </div>
                """, unsafe_allow_html=True)
            else:
                if st.button(label, key=f"nav_{doc_id}", use_container_width=True):
                    st.session_state.active_document_id = doc_id
                    st.session_state.workspace_view     = "overview"
                    st.rerun()

    if docs:
        st.markdown(
            f'<div style="font-size:12px;color:{RUST};margin-top:6px;cursor:pointer;'
            f'padding-left:4px;">View all documents →</div>',
            unsafe_allow_html=True
        )

    # ── TOOLS ───────────────────────────────────────────────────────────────
    st.markdown(
        '<div class="section-label" style="margin-top:22px;">Tools</div>',
        unsafe_allow_html=True
    )

    current_view = st.session_state.get("workspace_view", "overview")

    _tool_btn("👁  Overview",        "overview", current_view)
    _tool_btn("💬  Contextual Chat", "chat",     current_view)

    # AI Playground — coming soon
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:8px;padding:9px 12px;
                border:1.5px solid #E8E4DC;border-radius:9px;margin-bottom:4px;
                opacity:0.55;cursor:not-allowed;">
        <span style="font-size:13.5px;color:{FOREST};">✦  AI Playground</span>
        <span style="font-size:10px;font-weight:700;letter-spacing:0.8px;
                     background:{SAGE}20;color:{SAGE};padding:2px 7px;
                     border-radius:10px;border:1px solid {SAGE}40;">Soon</span>
    </div>
    """, unsafe_allow_html=True)

    # ── AI Ready card (bottom) ───────────────────────────────────────────────
    st.markdown("<div style='flex:1;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top:32px;'></div>", unsafe_allow_html=True)

    docs_exist   = bool(docs)
    active_doc   = docs.get(active_id, {}) if active_id else {}
    ai_ready     = active_doc.get("ai_ready", False) if docs_exist else False
    vs_ready     = active_doc.get("vector_store") is not None if docs_exist else False

    if docs_exist and ai_ready:
        st.markdown(f"""
        <div style="background:{WHITE};border:1.5px solid #C8E6C9;border-radius:12px;
                    padding:16px;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                <div style="width:20px;height:20px;background:#4CAF50;border-radius:50%;
                            display:flex;align-items:center;justify-content:center;
                            font-size:11px;color:white;font-weight:700;">✓</div>
                <span style="font-size:13.5px;font-weight:600;color:{FOREST};">AI Ready</span>
            </div>
            <div style="font-size:12px;color:#7A7772;line-height:1.5;">
                Your document is processed and ready for intelligent analysis.
            </div>
            <div style="font-size:11.5px;color:{RUST};margin-top:10px;cursor:pointer;font-weight:500;">
                Learn more →
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif docs_exist:
        st.markdown(f"""
        <div style="background:{WHITE};border:1.5px solid #E8E4DC;border-radius:12px;
                    padding:16px;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
                <div style="width:20px;height:20px;background:#FFA726;border-radius:50%;
                            display:flex;align-items:center;justify-content:center;
                            font-size:11px;color:white;">⚠</div>
                <span style="font-size:13px;font-weight:600;color:{FOREST};">Processing</span>
            </div>
            <div style="font-size:12px;color:#7A7772;line-height:1.5;">
                AI summary unavailable. Chat still works with raw text.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background:{WHITE};border:1.5px solid #E8E4DC;border-radius:12px;
                    padding:16px;">
            <div style="font-size:13px;font-weight:500;color:#B0ADA6;margin-bottom:4px;">No document loaded</div>
            <div style="font-size:12px;color:#B0ADA6;">Upload a file to begin.</div>
        </div>
        """, unsafe_allow_html=True)


def _tool_btn(label: str, view_key: str, current_view: str):
    """Render a tool navigation button with active state via custom HTML or Streamlit button."""
    is_active = (current_view == view_key)
    if is_active:
        st.markdown(f"""
        <div style="background:{FOREST}10;border:1.5px solid {FOREST}25;border-radius:9px;
                    padding:9px 12px;font-size:13.5px;font-weight:600;color:{FOREST};
                    margin-bottom:4px;">
            {label}
        </div>
        """, unsafe_allow_html=True)
    else:
        if st.button(label, key=f"tool_{view_key}", use_container_width=True):
            st.session_state.workspace_view = view_key
            st.rerun()
