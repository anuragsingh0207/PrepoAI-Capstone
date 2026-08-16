"""
workspace_view.py — Premium AI document workspace.

Layout matches the reference screenshot:
  ① Header: ← Back | filename | metadata row | ⭐ 📤 ⋯
  ② "What would you like to do?" — 3 action cards
  ③ Chat input bar + suggestion chips
  ④ Bottom panels: Document Overview (left) | AI Insights (right)
  ⑤ Security footer

Views driven by workspace_view session key:
  "overview"  → the main hub (this file)
  "summary"   → AI summary panel
  "mock_test" → mock test generator
  "chat"      → contextual RAG chat
"""
import time
import math
import json
import re
import traceback
import logging

import streamlit as st
from constants import FOREST, SAND, RUST, SAGE, CREAM, WHITE

logger = logging.getLogger("workspace_view")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s"
)


# ══════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════

def render():
    doc_id = st.session_state.get("active_document_id")
    docs   = st.session_state.get("uploaded_docs", {})

    if not doc_id or doc_id not in docs:
        _render_empty_state()
        return

    doc  = docs[doc_id]
    view = st.session_state.get("workspace_view", "overview")

    if view == "overview":
        _render_overview(doc, doc_id)
    elif view == "summary":
        _render_summary(doc, doc_id)
    elif view == "mock_test":
        _render_mock_test(doc, doc_id)
    elif view == "chat":
        _render_chat(doc, doc_id)
    else:
        _render_overview(doc, doc_id)


# ══════════════════════════════════════════════════════════
#  SHARED HEADER (used by all views)
# ══════════════════════════════════════════════════════════

def _render_header(doc: dict, doc_id: str, back_label: str = "Back to Workspace"):
    """Top header row: back link, filename, metadata chips, action icons."""
    name       = doc.get("name", "Document")
    ai_ready   = doc.get("ai_ready", False)
    char_count = doc.get("char_count", len(doc.get("text", "")))
    page_count = doc.get("page_count", "—")
    upload_ts  = doc.get("upload_time", time.time())
    vs_ready   = doc.get("vector_store") is not None

    # Time elapsed
    elapsed = time.time() - upload_ts
    if elapsed < 120:
        when = "Just now"
    elif elapsed < 3600:
        when = f"{int(elapsed/60)}m ago"
    else:
        when = f"{int(elapsed/3600)}h ago"

    status_color  = "#4CAF50" if ai_ready else "#FFA726"
    status_label  = "AI Ready" if ai_ready else "Processing"

    # ── Back link ────────────────────────────────────────
    back_col, _ = st.columns([1, 5])
    with back_col:
        if st.button(f"← {back_label}", key="btn_back_header"):
            st.session_state.workspace_view = "overview"
            st.rerun()

    # ── Filename + metadata + icons ──────────────────────
    st.markdown(f"""
    <div style="display:flex;align-items:flex-start;justify-content:space-between;
                margin-top:4px;margin-bottom:6px;">
        <div style="flex:1;min-width:0;">
            <h1 style="font-family:'Playfair Display',serif;font-size:26px;font-weight:700;
                        color:{FOREST};margin:0 0 10px 0;line-height:1.2;
                        white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                {name}
            </h1>
            <div style="display:flex;flex-wrap:wrap;gap:16px;align-items:center;">
                <span style="font-size:12.5px;color:#9E9B96;">
                    📅 Uploaded {when}
                </span>
                <span style="font-size:12.5px;color:{status_color};font-weight:500;">
                    ✓ Status: {status_label}
                </span>
                <span style="font-size:12.5px;color:#9E9B96;">
                    📝 {char_count:,} characters
                </span>
                <span style="font-size:12.5px;color:#9E9B96;">
                    📄 {page_count} pages
                </span>
            </div>
        </div>
        <div style="display:flex;gap:8px;margin-left:16px;flex-shrink:0;margin-top:4px;">
            <div style="width:34px;height:34px;border:1.5px solid #E0DCD4;border-radius:8px;
                        display:flex;align-items:center;justify-content:center;
                        cursor:pointer;background:{WHITE};">⭐</div>
            <div style="width:34px;height:34px;border:1.5px solid #E0DCD4;border-radius:8px;
                        display:flex;align-items:center;justify-content:center;
                        cursor:pointer;background:{WHITE};">⬆</div>
            <div style="width:34px;height:34px;border:1.5px solid #E0DCD4;border-radius:8px;
                        display:flex;align-items:center;justify-content:center;
                        cursor:pointer;background:{WHITE};">⋯</div>
        </div>
    </div>
    <hr style="margin:16px 0 24px 0;border:none;border-top:1px solid #E8E4DC;">
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  OVERVIEW — main hub
# ══════════════════════════════════════════════════════════

def _render_overview(doc: dict, doc_id: str):
    _render_header(doc, doc_id, back_label="Workspace")

    # ── Action section heading ────────────────────────────
    st.markdown(f"""
    <div style="margin-bottom:6px;">
        <div style="font-family:'Playfair Display',serif;font-size:21px;font-weight:700;
                    color:{FOREST};margin-bottom:4px;">What would you like to do?</div>
        <div style="font-size:13.5px;color:#9E9B96;">
            Choose an option below or chat with your document
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 3 Action Cards ───────────────────────────────────
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        _action_card(
            icon="🗒",
            icon_bg="#EDF7ED",
            title="Summarize PDF",
            desc="Get a concise summary of the entire document with key insights and takeaways.",
            btn_key="card_summary",
            view_target="summary"
        )

    with c2:
        _action_card(
            icon="📋",
            icon_bg="#EEF0FF",
            title="Create Mock Test",
            desc="Generate a mock test with important questions based on the content of this document.",
            btn_key="card_mock",
            view_target="mock_test"
        )

    with c3:
        _action_card(
            icon="💬",
            icon_bg="#E8F4FF",
            title="Chat with PDF",
            desc="Ask questions and get answers from your document using AI.",
            btn_key="card_chat",
            view_target="chat"
        )

    # ── Chat input + suggestion chips ────────────────────
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    _render_chat_input_bar(doc, doc_id)

    # ── Bottom panels ─────────────────────────────────────
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    _render_bottom_panels(doc)

    # ── Security footer ───────────────────────────────────
    st.markdown(f"""
    <div style="text-align:center;margin-top:32px;padding:12px 0;
                border-top:1px solid #E8E4DC;">
        <span style="font-size:12px;color:#B0ADA6;">
            🔒 Your document and conversations are secure and private.
        </span>
    </div>
    """, unsafe_allow_html=True)


def _action_card(icon, icon_bg, title, desc, btn_key, view_target):
    """Render a premium action card matching the reference design."""
    st.markdown(f"""
    <div style="background:{WHITE};border:1.5px solid #E8E4DC;border-radius:14px;
                padding:20px;min-height:160px;position:relative;
                box-shadow:0 2px 8px rgba(0,0,0,0.04);
                transition:box-shadow 0.2s;">
        <div style="width:42px;height:42px;background:{icon_bg};border-radius:10px;
                    display:flex;align-items:center;justify-content:center;
                    font-size:20px;margin-bottom:14px;">{icon}</div>
        <div style="font-size:14.5px;font-weight:600;color:{FOREST};margin-bottom:6px;">{title}</div>
        <div style="font-size:12.5px;color:#9E9B96;line-height:1.6;margin-bottom:14px;">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("→", key=btn_key, use_container_width=True):
        st.session_state.workspace_view = view_target
        st.rerun()


def _render_chat_input_bar(doc: dict, doc_id: str):
    """Full-width chat bar with suggestion chips below."""

    # Input
    if user_msg := st.chat_input("Ask anything about your document...", key="overview_chat"):
        # Pre-fill and jump to chat view
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = {}
        if doc_id not in st.session_state.chat_messages:
            st.session_state.chat_messages[doc_id] = []
        st.session_state.chat_messages[doc_id].append({"role": "user", "content": user_msg})
        st.session_state._pending_chat_msg = user_msg
        st.session_state.workspace_view = "chat"
        st.rerun()

    # Suggestion chips
    st.markdown(f"""
    <div style="margin-top:10px;">
        <span style="font-size:12.5px;color:#9E9B96;margin-right:10px;">Try these examples:</span>
    </div>
    """, unsafe_allow_html=True)

    suggestions = [
        "What is the main topic?",
        "List key points",
        "Explain in simple terms",
        "Important definitions",
    ]
    chip_cols = st.columns(len(suggestions))
    for i, (col, suggestion) in enumerate(zip(chip_cols, suggestions)):
        with col:
            if st.button(suggestion, key=f"chip_{i}"):
                if "chat_messages" not in st.session_state:
                    st.session_state.chat_messages = {}
                if doc_id not in st.session_state.chat_messages:
                    st.session_state.chat_messages[doc_id] = []
                st.session_state.chat_messages[doc_id].append({"role": "user", "content": suggestion})
                st.session_state._pending_chat_msg = suggestion
                st.session_state.workspace_view = "chat"
                st.rerun()


def _render_bottom_panels(doc: dict):
    """Two-column: Document Overview (left) + AI Insights (right)."""
    left, right = st.columns(2, gap="large")

    name       = doc.get("name", "—")
    char_count = doc.get("char_count", len(doc.get("text", "")))
    page_count = doc.get("page_count", "—")
    upload_ts  = doc.get("upload_time", time.time())
    ai_ready   = doc.get("ai_ready", False)
    topics     = doc.get("topics", [])
    text       = doc.get("text", "")

    # Rough file-size estimate
    size_kb = len(text.encode("utf-8")) / 1024
    size_str = f"{size_kb:.1f} KB" if size_kb < 1024 else f"{size_kb/1024:.1f} MB"

    import datetime
    upload_dt = datetime.datetime.fromtimestamp(upload_ts).strftime("%d %b %Y, %H:%M")

    # Complexity heuristic
    avg_word_len = sum(len(w) for w in text.split()) / max(len(text.split()), 1)
    if avg_word_len > 6.5:
        complexity = "Advanced"
    elif avg_word_len > 5.2:
        complexity = "Intermediate"
    else:
        complexity = "Beginner"

    # Question potential
    q_keywords = ["define", "explain", "compare", "describe", "what", "how", "why",
                  "formula", "example", "derive", "prove", "calculate"]
    q_score = sum(1 for kw in q_keywords if kw.lower() in text.lower())
    q_potential = "High" if q_score >= 6 else ("Medium" if q_score >= 3 else "Low")

    with left:
        st.markdown(f"""
        <div style="background:{WHITE};border:1.5px solid #E8E4DC;border-radius:14px;
                    padding:22px;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
            <div style="font-size:15px;font-weight:600;color:{FOREST};margin-bottom:18px;">
                Document Overview
            </div>
            {_info_row("File Name",   name[:40] + ("…" if len(name) > 40 else ""))}
            {_info_row("Upload Date", upload_dt)}
            {_info_row("File Size",   size_str)}
            {_info_row("Pages",       str(page_count))}
            {_info_row("Characters",  f"{char_count:,}")}
            {_info_row("Status",      _status_badge(ai_ready))}
        </div>
        """, unsafe_allow_html=True)

    with right:
        topic_html = ""
        if topics:
            chips = "".join([
                f'<span style="background:#F5F5F0;border:1px solid #E0DCD4;'
                f'border-radius:14px;padding:3px 10px;font-size:12px;'
                f'color:{FOREST};margin-right:4px;">{t}</span>'
                for t in topics[:2]
            ])
            more = f' <span style="font-size:12px;color:#9E9B96;">+ {len(topics)-2} more</span>' if len(topics) > 2 else ""
            topic_html = chips + more
        else:
            topic_html = '<span style="font-size:12.5px;color:#B0ADA6;">—</span>'

        sum_status = "Ready" if ai_ready else "Unavailable"
        sum_color  = "#4CAF50" if ai_ready else "#FFA726"

        st.markdown(f"""
        <div style="background:{WHITE};border:1.5px solid #E8E4DC;border-radius:14px;
                    padding:22px;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
            <div style="font-size:15px;font-weight:600;color:{FOREST};margin-bottom:18px;">
                ✦ AI Insights
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:9px 0;border-bottom:1px solid #F0EDE8;">
                <span style="font-size:13px;color:#7A7772;">Key Topics</span>
                <span>{topic_html}</span>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:9px 0;border-bottom:1px solid #F0EDE8;">
                <span style="font-size:13px;color:#7A7772;">Complexity</span>
                <span style="font-size:13px;font-weight:600;color:{FOREST};">{complexity}</span>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:9px 0;border-bottom:1px solid #F0EDE8;">
                <span style="font-size:13px;color:#7A7772;">Question Potential</span>
                <span style="font-size:13px;font-weight:600;color:{FOREST};">{q_potential}</span>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:9px 0;">
                <span style="font-size:13px;color:#7A7772;">Summary Status</span>
                <span style="background:{sum_color}20;color:{sum_color};font-size:12px;
                             font-weight:600;padding:3px 10px;border-radius:12px;
                             border:1px solid {sum_color}40;">{sum_status}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


def _info_row(label: str, value: str) -> str:
    return f"""
    <div style="display:flex;justify-content:space-between;align-items:center;
                padding:8px 0;border-bottom:1px solid #F0EDE8;">
        <span style="font-size:13px;color:#7A7772;">{label}</span>
        <span style="font-size:13px;color:{FOREST};font-weight:500;">{value}</span>
    </div>
    """


def _status_badge(ai_ready: bool) -> str:
    if ai_ready:
        return f'<span style="background:#E8F5E9;color:#4CAF50;font-size:12px;font-weight:600;padding:3px 10px;border-radius:12px;border:1px solid #C8E6C9;">AI Ready</span>'
    return f'<span style="background:#FFF3E0;color:#FFA726;font-size:12px;font-weight:600;padding:3px 10px;border-radius:12px;border:1px solid #FFE0B2;">Processing</span>'


# ══════════════════════════════════════════════════════════
#  SUMMARY VIEW
# ══════════════════════════════════════════════════════════

# Visual config per level — colours, icons, descriptors
_LEVEL_META = {
    "quick": {
        "label":      "Quick Overview",
        "icon":       "📘",
        "badge_bg":   "#E8F4FD",
        "badge_fg":   "#1976D2",
        "desc":       "Fast executive summary — main ideas in 60 seconds",
        "spinner":    "⚡ Generating quick overview...",
        "time_est":   "~5 seconds",
    },
    "standard": {
        "label":      "Standard Summary",
        "icon":       "📗",
        "badge_bg":   "#E8F5E9",
        "badge_fg":   "#388E3C",
        "desc":       "Structured educational summary — concepts, definitions & key points",
        "spinner":    "🧠 Building structured summary...",
        "time_est":   "~15 seconds",
    },
    "deep": {
        "label":      "In-Depth Analysis",
        "icon":       "📙",
        "badge_bg":   "#FFF3E0",
        "badge_fg":   "#E65100",
        "desc":       "Comprehensive academic analysis — architecture, insights & revision table",
        "spinner":    "🔬 Running deep analysis...",
        "time_est":   "~30 seconds",
    },
}


def _render_summary(doc: dict, doc_id: str):
    _render_header(doc, doc_id)

    st.markdown(f"""
    <div style="font-family:'Playfair Display',serif;font-size:20px;font-weight:700;
                color:{FOREST};margin-bottom:4px;">AI Document Summary</div>
    <div style="font-size:13.5px;color:#9E9B96;margin-bottom:20px;">
        Three genuinely different AI pipelines — each with unique depth, structure, and retrieval strategy
    </div>
    """, unsafe_allow_html=True)

    # ── Level selector ────────────────────────────────────────────────────────
    # Maps display label → internal routing key
    LEVEL_OPTIONS = {
        "📘  Quick Overview":    "quick",
        "📗  Standard Summary":  "standard",
        "📙  In-Depth Analysis": "deep",
    }

    selected_label = st.radio(
        "Summary depth",
        list(LEVEL_OPTIONS.keys()),
        horizontal=True,
        label_visibility="collapsed",
        key="summary_level_radio"
    )
    level = LEVEL_OPTIONS[selected_label]
    meta  = _LEVEL_META[level]

    # ── Level description card ────────────────────────────────────────────────
    strategy_txt = (
        "🔍 RAG-augmented retrieval" if doc.get("vector_store") and level != "quick"
        else "📄 Raw text context"
    )
    st.markdown(f"""
    <div style="background:{meta['badge_bg']};border-radius:10px;padding:12px 16px;
                margin-bottom:20px;display:flex;align-items:center;gap:12px;
                border:1px solid {meta['badge_fg']}30;">
        <span style="font-size:22px;">{meta['icon']}</span>
        <div>
            <div style="font-size:13.5px;font-weight:600;color:{meta['badge_fg']};">{meta['label']}</div>
            <div style="font-size:12px;color:#7A7772;margin-top:2px;">
                {meta['desc']} &nbsp;·&nbsp; {strategy_txt} &nbsp;·&nbsp; Est. {meta['time_est']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Generate button ───────────────────────────────────────────────────────
    cache_key = f"summary_{doc_id}_{level}"
    stored    = st.session_state.get(cache_key)

    col_btn, col_regen, _ = st.columns([1.5, 1.5, 3])
    with col_btn:
        generate_clicked = st.button(
            f"✦ Generate {meta['label']}", type="primary",
            key=f"btn_gen_{level}", use_container_width=True
        )
    with col_regen:
        if stored:
            if st.button("↺ Regenerate", key=f"btn_regen_{level}", use_container_width=True):
                st.session_state.pop(cache_key, None)
                generate_clicked = True

    if generate_clicked:
        _generate_summary(doc, doc_id, level, meta)
        return   # _generate_summary calls st.rerun() on success

    # ── Render stored result ──────────────────────────────────────────────────
    if stored:
        _render_summary_result(stored, level, meta, doc_id)

    elif not stored and doc.get("summary") and "Could not" not in doc.get("summary",""):
        # Fall back to the upload-time quick summary for the quick level only
        if level == "quick":
            _render_upload_summary_fallback(doc)
        else:
            st.markdown(f"""
            <div style="background:{WHITE};border:1.5px solid #E8E4DC;border-radius:12px;
                        padding:24px;text-align:center;color:#9E9B96;">
                <div style="font-size:28px;margin-bottom:8px;">{meta['icon']}</div>
                <div style="font-size:14px;font-weight:500;color:{FOREST};">
                    {meta['label']} not generated yet
                </div>
                <div style="font-size:13px;margin-top:6px;">
                    Click <strong>Generate {meta['label']}</strong> above to run the AI pipeline.
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background:{WHITE};border:1.5px solid #E8E4DC;border-radius:12px;
                    padding:24px;text-align:center;color:#9E9B96;">
            <div style="font-size:28px;margin-bottom:8px;">{meta['icon']}</div>
            <div style="font-size:14px;font-weight:500;color:{FOREST};">Ready to generate</div>
            <div style="font-size:13px;margin-top:6px;">
                Click <strong>Generate {meta['label']}</strong> to start the AI pipeline.
            </div>
        </div>
        """, unsafe_allow_html=True)


def _render_summary_result(content: str, level: str, meta: dict, doc_id: str):
    """Render the generated summary with level-appropriate visual styling."""
    word_count = len(content.split())
    char_count = len(content)

    st.markdown(f"""
    <div style="display:flex;align-items:center;justify-content:space-between;
                margin-bottom:12px;margin-top:4px;">
        <div style="display:flex;align-items:center;gap:8px;">
            <span style="background:{meta['badge_bg']};color:{meta['badge_fg']};
                         font-size:11.5px;font-weight:700;padding:3px 10px;
                         border-radius:12px;border:1px solid {meta['badge_fg']}30;">
                {meta['icon']} {meta['label']}
            </span>
        </div>
        <div style="font-size:12px;color:#9E9B96;">
            ~{word_count:,} words &nbsp;·&nbsp; {char_count:,} characters
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Use Streamlit's native markdown renderer (not HTML) for proper heading/table rendering
    with st.container():
        st.markdown(
            f'<div style="background:{WHITE};border:1.5px solid #E8E4DC;border-radius:14px;'
            f'padding:28px 32px;box-shadow:0 2px 8px rgba(0,0,0,0.04);">',
            unsafe_allow_html=True
        )
        st.markdown(content)
        st.markdown("</div>", unsafe_allow_html=True)

    # Copy / export area
    with st.expander("📋 Export / Copy raw text"):
        st.text_area(
            "Summary text",
            value=content,
            height=200,
            label_visibility="collapsed",
            key=f"export_{doc_id}_{level}"
        )


def _render_upload_summary_fallback(doc: dict):
    """Show the quick summary that was generated at upload time."""
    summary = doc.get("summary", "")
    topics  = doc.get("topics", [])
    topic_html = "".join([
        f'<span style="background:#F5F5F0;border:1px solid #E0DCD4;border-radius:14px;'
        f'padding:4px 12px;font-size:12.5px;color:{FOREST};margin-right:6px;">{t}</span>'
        for t in topics
    ])
    st.markdown(f"""
    <div style="background:{WHITE};border:1.5px solid #E8E4DC;border-radius:14px;
                padding:26px;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
        <div style="font-size:12px;font-weight:700;color:#9E9B96;text-transform:uppercase;
                    letter-spacing:1px;margin-bottom:12px;">Quick Overview (from upload)</div>
        <div style="font-size:14.5px;color:{FOREST};line-height:1.8;">{summary}</div>
        <div style="margin-top:16px;padding-top:14px;border-top:1px solid #F0EDE8;">
            <div style="font-size:13px;font-weight:600;color:{FOREST};margin-bottom:8px;">Key Topics</div>
            <div>{topic_html}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.info("💡 Click **Generate Quick Overview** above to get a freshly structured AI summary.")


def _generate_summary(doc: dict, doc_id: str, level: str, meta: dict):
    """
    Dispatch to the production-grade summarization pipeline.
    Each level routes to a different prompt, LLM config, and retrieval strategy.
    """
    from backend.summarizer import run_summary_pipeline

    text         = doc.get("text", "")
    vector_store = doc.get("vector_store")
    doc_name     = doc.get("name", "document")

    logger.info(f"[SUMMARY UI] Dispatching level='{level}' for doc='{doc_name}'")

    with st.spinner(meta["spinner"]):
        result = run_summary_pipeline(
            level=level,
            text=text,
            vector_store=vector_store,
            doc_name=doc_name
        )

    if result["error"]:
        error = result["error"]
        if error == "empty_document":
            st.error("❌ Document has no extractable text. Please re-upload the file.")
        elif error == "missing_api_key":
            st.error("❌ GROQ_API_KEY is missing. Cannot generate summary.")
        else:
            st.error(
                f"❌ Summary generation failed.\n\n"
                f"**Error:** {error[:300]}\n\n"
                "Please try again. If the error persists, check terminal logs."
            )
        logger.error(f"[SUMMARY UI] Pipeline returned error: {error}")
        return

    if not result["content"].strip():
        st.error("❌ AI returned an empty response. Please try again.")
        return

    cache_key = f"summary_{doc_id}_{level}"
    st.session_state[cache_key] = result["content"]
    logger.info(
        f"[SUMMARY UI] Stored: level={level}, {result['char_count']} chars, "
        f"strategy={result['strategy']}"
    )
    st.rerun()



# ══════════════════════════════════════════════════════════
#  MOCK TEST VIEW
# ══════════════════════════════════════════════════════════

def _render_mock_test(doc: dict, doc_id: str):
    _render_header(doc, doc_id)

    st.markdown(f"""
    <div style="font-family:'Playfair Display',serif;font-size:20px;font-weight:700;
                color:{FOREST};margin-bottom:4px;">Create Mock Test</div>
    <div style="font-size:13.5px;color:#9E9B96;margin-bottom:24px;">
        AI-generated questions from your document
    </div>
    """, unsafe_allow_html=True)

    # ── Configuration ─────────────────────────────────────
    cfg_col, _ = st.columns([2, 1])
    with cfg_col:
        with st.container():
            st.markdown(f"""
            <div style="background:{WHITE};border:1.5px solid #E8E4DC;border-radius:14px;
                        padding:22px;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
                <div style="font-size:14px;font-weight:600;color:{FOREST};margin-bottom:16px;">
                    Test Configuration
                </div>
            </div>
            """, unsafe_allow_html=True)

        num_q      = st.slider("Number of questions", 3, 20, 10, key="mt_num_q")
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard", "Mixed"], index=1, key="mt_diff")
        q_type     = st.selectbox("Question type", ["MCQ", "Short Answer", "True/False", "Mixed"], key="mt_type")

        col_gen, col_clear = st.columns(2)
        with col_gen:
            if st.button("⚡ Generate Test", type="primary", key="btn_gen_test", use_container_width=True):
                _generate_mock_test(doc, num_q, difficulty, q_type)
        with col_clear:
            if st.button("🗑 Clear", key="btn_clear_test", use_container_width=True):
                st.session_state.pop(f"mocktest_{doc_id}", None)
                st.rerun()

    # ── Show questions ────────────────────────────────────
    questions = st.session_state.get(f"mocktest_{doc_id}", [])
    if not questions:
        return

    st.markdown(f"""
    <div style="font-size:14px;font-weight:600;color:{FOREST};
                margin-top:28px;margin-bottom:16px;">
        {len(questions)} Questions Generated
    </div>
    """, unsafe_allow_html=True)

    for i, q in enumerate(questions, 1):
        # Support both snake_case (correct_answer) and camelCase (correctAnswer)
        q_text  = q.get("question", "")
        q_type_ = q.get("type", "mcq").lower()
        opts    = q.get("options", [])
        correct = q.get("correct_answer") or q.get("correctAnswer", "")
        explain = q.get("explanation", "")
        topic_  = q.get("topic", "")
        diff_   = q.get("difficulty", "")

        if not q_text:
            continue  # skip malformed entries

        label = f"Q{i}. {q_text[:90]}{'…' if len(q_text) > 90 else ''}"
        with st.expander(label, expanded=(i <= 3)):
            st.markdown(f"**{q_text}**")

            row_meta = []
            if topic_:
                row_meta.append(f"📌 {topic_}")
            if diff_:
                row_meta.append(f"🎯 {diff_.title()}")
            if row_meta:
                st.caption(" · ".join(row_meta))

            if opts:
                for opt in opts:
                    opt_str      = str(opt).strip()
                    correct_str  = str(correct).strip()
                    # Match if option starts with the correct answer letter prefix
                    is_correct = (
                        opt_str.lower() == correct_str.lower()
                        or (len(correct_str) >= 2 and opt_str.lower().startswith(correct_str[:2].lower()))
                        or correct_str.lower() in opt_str.lower()
                    )
                    icon = "✅" if is_correct else "◦"
                    st.markdown(f"{icon} {opt_str}")

            if correct:
                st.success(f"**Correct Answer:** {correct}")
            if explain:
                st.info(f"💡 **Explanation:** {explain}")


# ──────────────────────────────────────────────────────────────────────────────
#  JSON REPAIR UTILITIES
# ──────────────────────────────────────────────────────────────────────────────

def _strip_fences(raw: str) -> str:
    """Remove markdown code fences (```json ... ```) robustly."""
    raw = raw.strip()
    # Remove opening fence
    if raw.startswith("```"):
        first_nl = raw.find("\n")
        raw = raw[first_nl + 1:] if first_nl != -1 else raw[3:]
    # Remove closing fence
    if raw.endswith("```"):
        raw = raw[:-3].strip()
    return raw.strip()


def _extract_json_block(raw: str) -> str:
    """
    Try to extract a valid JSON object from a response that may contain
    surrounding prose. Finds the outermost { ... } block.
    """
    start = raw.find("{")
    end   = raw.rfind("}")
    if start != -1 and end != -1 and end > start:
        return raw[start : end + 1]
    return raw


def _parse_questions_robust(raw: str) -> list[dict]:
    """
    Multi-strategy JSON parser. Tries 4 strategies in order:
      1. Direct parse after fence stripping
      2. Extract outermost JSON object then parse
      3. Regex-extract the questions array directly
      4. Return empty list (never crash)

    Logs the raw response and each failure for full debug visibility.
    """
    logger.info(f"[JSON PARSE] Raw response length: {len(raw)} chars")
    logger.debug(f"[JSON PARSE] Raw (first 500):\n{raw[:500]}")

    # Strategy 1: strip fences + direct parse
    try:
        cleaned = _strip_fences(raw)
        data    = json.loads(cleaned)
        qs      = _extract_questions_from_data(data)
        logger.info(f"[JSON PARSE] Strategy 1 succeeded: {len(qs)} questions")
        return qs
    except Exception as e:
        logger.warning(f"[JSON PARSE] Strategy 1 failed: {e}")

    # Strategy 2: extract outermost JSON object
    try:
        block   = _extract_json_block(raw)
        data    = json.loads(block)
        qs      = _extract_questions_from_data(data)
        logger.info(f"[JSON PARSE] Strategy 2 succeeded: {len(qs)} questions")
        return qs
    except Exception as e:
        logger.warning(f"[JSON PARSE] Strategy 2 failed: {e}")

    # Strategy 3: regex extract questions array
    try:
        match = re.search(r'"questions"\s*:\s*(\[.*?\])', raw, re.DOTALL)
        if match:
            arr = json.loads(match.group(1))
            if isinstance(arr, list):
                logger.info(f"[JSON PARSE] Strategy 3 succeeded: {len(arr)} questions")
                return arr
    except Exception as e:
        logger.warning(f"[JSON PARSE] Strategy 3 failed: {e}")

    # Strategy 4: try json_repair if installed
    try:
        from json_repair import repair_json  # type: ignore
        repaired = repair_json(raw)
        data     = json.loads(repaired)
        qs       = _extract_questions_from_data(data)
        logger.info(f"[JSON PARSE] Strategy 4 (json_repair) succeeded: {len(qs)} questions")
        return qs
    except Exception as e:
        logger.warning(f"[JSON PARSE] Strategy 4 failed: {e}")

    logger.error(f"[JSON PARSE] ALL STRATEGIES FAILED. Raw response:\n{raw}")
    return []


def _extract_questions_from_data(data: dict | list) -> list[dict]:
    """Extract and validate the questions list from parsed JSON."""
    if isinstance(data, list):
        questions = data
    elif isinstance(data, dict):
        questions = data.get("questions", data.get("Questions", []))
    else:
        return []

    validated = []
    for i, q in enumerate(questions):
        if not isinstance(q, dict):
            continue
        if not q.get("question") and not q.get("Question"):
            logger.warning(f"[SCHEMA] Question {i} missing 'question' field — skipping")
            continue
        # Normalise camelCase → snake_case
        if "correctAnswer" in q and "correct_answer" not in q:
            q["correct_answer"] = q["correctAnswer"]
        if "Question" in q and "question" not in q:
            q["question"] = q["Question"]
        validated.append(q)

    return validated


# ──────────────────────────────────────────────────────────────────────────────
#  MOCK TEST GENERATOR — PRODUCTION GRADE
# ──────────────────────────────────────────────────────────────────────────────

def _generate_mock_test(doc: dict, num_q: int, difficulty: str, q_type: str):
    """
    Production-grade mock test generator.

    ROOT CAUSE FIX:
    The previous code used ChatPromptTemplate with {{text}} in the human
    message. LangChain's template engine treats {{text}} as an escaped literal
    (not a variable), so input_variables = [] and the document text was NEVER
    injected into the prompt. The LLM generated questions from an EMPTY context.

    FIX: Use SystemMessage + HumanMessage directly (no template engine),
    building the human message as a plain Python f-string.

    Additional fixes:
    - Multi-strategy JSON parser (4 fallbacks)
    - Retry with exponential back-off (3 attempts)
    - Full structured logging at every stage
    - Schema validation and field normalisation
    """
    from backend.intelligence import _get_llm
    from langchain_core.messages import SystemMessage, HumanMessage

    doc_id   = st.session_state.get("active_document_id", "")
    text_raw = doc.get("text", "")
    name     = doc.get("name", "document")

    # ── Pre-flight checks ──────────────────────────────────
    logger.info(f"[MOCK] Generation requested: doc='{name}' num_q={num_q} difficulty={difficulty} type={q_type}")

    llm = _get_llm()
    if not llm:
        st.error("❌ GROQ_API_KEY missing. Cannot generate test.")
        logger.error("[MOCK] LLM init failed: no API key")
        return

    if not text_raw.strip():
        st.error("❌ Document text is empty. Please re-upload the file.")
        logger.error("[MOCK] Empty document text — aborting")
        return

    # Truncate to 8000 chars; that's ~2000 tokens — safe for Groq context
    text_in  = text_raw[:8000]
    type_map = {"MCQ": "mcq", "Short Answer": "short_answer", "True/False": "true_false", "Mixed": "mixed"}
    qtype_key = type_map.get(q_type, "mcq")

    logger.info(f"[MOCK] Text length: {len(text_in)} chars | qtype_key: {qtype_key}")

    # ── Production-grade system prompt ────────────────────
    # CRITICAL: No f-string template variables here — this is a plain string
    # passed as SystemMessage content. The document text goes into HumanMessage.
    SYSTEM_PROMPT = (
        f"You are a world-class exam paper setter with expertise in generating "
        f"{difficulty.lower()}-difficulty academic questions.\n\n"
        f"TASK: Generate EXACTLY {num_q} {qtype_key} questions based ONLY on the "
        f"document the user provides.\n\n"
        "=== STRICT RULES ===\n"
        "1. Use ONLY content from the provided document. Never hallucinate.\n"
        "2. Each question must test a DIFFERENT concept from the document.\n"
        "3. Questions must be exam-quality — clear, unambiguous, educational.\n"
        "4. For MCQ: provide exactly 4 options labeled A, B, C, D. Exactly one is correct.\n"
        "5. For short_answer: provide a model answer of 2-4 sentences.\n"
        "6. For true_false: the statement must be unambiguously true or false.\n"
        "7. For mixed: distribute evenly across mcq, short_answer, true_false.\n\n"
        "=== OUTPUT FORMAT ===\n"
        "Return ONLY a raw JSON object. No markdown. No backticks. No prose before or after.\n"
        "Start your response with { and end with }.\n\n"
        "Required schema:\n"
        "{\n"
        '  "questions": [\n'
        "    {\n"
        '      "id": 1,\n'
        '      "type": "mcq",\n'
        '      "question": "Full question text here",\n'
        '      "options": ["A. First option", "B. Second option", "C. Third option", "D. Fourth option"],\n'
        '      "correct_answer": "A. First option",\n'
        '      "explanation": "Why this answer is correct, in 1-2 sentences",\n'
        '      "topic": "Sub-topic from the document",\n'
        f'      "difficulty": "{difficulty.lower()}"\n'
        "    }\n"
        "  ]\n"
        "}"
    )

    logger.info(f"[MOCK] System prompt length: {len(SYSTEM_PROMPT)} chars")

    # ── Retry loop ─────────────────────────────────────────
    MAX_ATTEMPTS = 3
    last_error   = None
    questions    = []

    with st.spinner(f"⚡ Generating {num_q} {difficulty} questions..."):
        for attempt in range(1, MAX_ATTEMPTS + 1):
            logger.info(f"[MOCK] Attempt {attempt}/{MAX_ATTEMPTS}")
            try:
                # ✅ FIX: SystemMessage + HumanMessage — document text injected here
                sys_msg  = SystemMessage(content=SYSTEM_PROMPT)
                user_msg = HumanMessage(
                    content=(
                        f"Generate {num_q} questions from this document.\n\n"
                        f"Document title: {name}\n"
                        f"Document content:\n\n{text_in}"
                    )
                )

                logger.info(f"[MOCK] Calling LLM (attempt {attempt})...")
                resp = llm.invoke([sys_msg, user_msg])
                raw  = resp.content

                logger.info(f"[MOCK] LLM response received: {len(raw)} chars")
                logger.debug(f"[MOCK] Raw response (first 400):\n{raw[:400]}")

                # ── Multi-strategy JSON parsing ────────────
                questions = _parse_questions_robust(raw)

                if not questions:
                    raise ValueError(
                        f"Parser returned 0 questions. Raw response:\n{raw[:300]}"
                    )

                logger.info(f"[MOCK] Success: {len(questions)} questions parsed on attempt {attempt}")
                break  # success — exit retry loop

            except Exception as e:
                last_error = e
                full_tb    = traceback.format_exc()
                logger.error(f"[MOCK] Attempt {attempt} failed:\n{full_tb}")

                if attempt < MAX_ATTEMPTS:
                    wait = 2 ** attempt  # 2s, 4s back-off
                    logger.info(f"[MOCK] Retrying in {wait}s...")
                    import time as _time
                    _time.sleep(wait)
                else:
                    logger.error(f"[MOCK] All {MAX_ATTEMPTS} attempts exhausted.")

    # ── Result handling ────────────────────────────────────
    if questions:
        st.session_state[f"mocktest_{doc_id}"] = questions
        logger.info(f"[MOCK] Stored {len(questions)} questions in session state")
        st.rerun()
    else:
        err_detail = str(last_error)[:200] if last_error else "Unknown error"
        st.error(
            f"❌ Test generation failed after {MAX_ATTEMPTS} attempts.\n"
            f"**Error:** {err_detail}\n\n"
            "Possible causes:\n"
            "- Document text is too short or not informative enough\n"
            "- Groq API rate limit reached (try again in 30s)\n"
            "- LLM returned non-JSON output (see terminal logs)"
        )
        logger.error(f"[MOCK] Final failure: {last_error}")


# ══════════════════════════════════════════════════════════
#  CHAT VIEW — RAG-powered contextual chat
# ══════════════════════════════════════════════════════════

def _render_chat(doc: dict, doc_id: str):
    _render_header(doc, doc_id)

    vector_store = doc.get("vector_store")
    mode_badge   = "🔍 RAG Mode" if vector_store else "📝 Text Mode"

    st.markdown(f"""
    <div style="font-family:'Playfair Display',serif;font-size:20px;font-weight:700;
                color:{FOREST};margin-bottom:4px;">Chat with PDF</div>
    <div style="font-size:13px;color:#9E9B96;margin-bottom:20px;">
        {mode_badge} — {"Answers retrieved via vector similarity search" if vector_store else "Using first 8,000 characters as context"}
    </div>
    """, unsafe_allow_html=True)

    # Initialise history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = {}
    if doc_id not in st.session_state.chat_messages:
        st.session_state.chat_messages[doc_id] = [
            {"role": "assistant",
             "content": f"Hi! I've read **{doc.get('name','')}**. Ask me anything about it — I'll answer only from the document."}
        ]

    messages = st.session_state.chat_messages[doc_id]

    # Clear chat button
    c_clear, _ = st.columns([1, 5])
    with c_clear:
        if st.button("🗑 Clear chat", key="btn_clear_chat"):
            st.session_state.chat_messages[doc_id] = [
                {"role": "assistant", "content": "Chat cleared. Ask me anything!"}
            ]
            st.rerun()

    # Render history
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Handle any pending message from overview chips
    pending = st.session_state.pop("_pending_chat_msg", None)
    if pending and (not messages or messages[-1]["content"] != pending):
        _handle_chat_message(pending, doc, doc_id, messages)
        st.rerun()

    # Chat input
    if prompt := st.chat_input("Ask a question about your document...", key="chat_view_input"):
        _handle_chat_message(prompt, doc, doc_id, messages)
        st.rerun()


def _handle_chat_message(prompt: str, doc: dict, doc_id: str, messages: list):
    """Process user message through RAG pipeline and append response."""
    st.chat_message("user").markdown(prompt)
    messages.append({"role": "user", "content": prompt})

    from backend.intelligence import _get_llm
    from langchain_core.messages import HumanMessage, SystemMessage

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("✦ Thinking...")

        try:
            llm = _get_llm()
            if not llm:
                response = "❌ Cannot answer — GROQ_API_KEY is missing."
            else:
                vector_store = doc.get("vector_store")
                context_text = ""

                if vector_store is not None:
                    context_text = _retrieve_context(vector_store, prompt)
                    if not context_text:
                        context_text = doc.get("text", "")[:8000]
                else:
                    context_text = doc.get("text", "")[:8000]

                RAG_CHAT_PROMPT = f"""\
You are a precise, context-grounded AI study assistant for the document: "{doc.get('name','')}".

=== STRICT RULES ===
1. Answer ONLY from the document context provided below.
2. If the answer is not in the context, say exactly:
   "This information is not available in the uploaded document."
3. NEVER hallucinate, invent, or use outside knowledge.
4. Be concise but complete.
5. Use bullet points for lists.
6. Bold key terms.
7. If asked to explain, use a simple analogy then the technical explanation.
8. If the user asks a follow-up, use the chat history to maintain context.

=== DOCUMENT CONTEXT ===
{context_text}
"""

                sys_msg  = SystemMessage(content=RAG_CHAT_PROMPT)
                user_msg = HumanMessage(content=prompt)
                resp     = llm.invoke([sys_msg, user_msg])
                response = resp.content

        except Exception:
            logger.error(traceback.format_exc())
            response = "❌ An error occurred. Please try again."

        placeholder.markdown(response)
        messages.append({"role": "assistant", "content": response})


def _retrieve_context(vector_store, query: str, k: int = 5) -> str:
    try:
        retriever = vector_store.as_retriever(search_kwargs={"k": k})
        docs      = retriever.invoke(query)
        if not docs:
            return ""
        return "\n\n".join(f"[Passage {i+1}]\n{d.page_content}" for i, d in enumerate(docs))
    except Exception:
        logger.error(f"Retrieval failed:\n{traceback.format_exc()}")
        return ""


# ══════════════════════════════════════════════════════════
#  EMPTY STATE
# ══════════════════════════════════════════════════════════

def _render_empty_state():
    st.markdown(f"""
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
                min-height:60vh;text-align:center;">
        <div style="font-size:48px;margin-bottom:16px;">📄</div>
        <div style="font-family:'Playfair Display',serif;font-size:22px;font-weight:700;
                    color:{FOREST};margin-bottom:8px;">No document selected</div>
        <div style="font-size:14px;color:#9E9B96;max-width:320px;line-height:1.6;margin-bottom:24px;">
            Upload a PDF or select a document from the sidebar to get started.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("📤 Upload New File", type="primary", use_container_width=True):
            st.session_state.app_mode = "upload"
            st.rerun()
