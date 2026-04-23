import sys, os as _os
_UI_DIR = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), ".."))
if _UI_DIR not in sys.path:
    sys.path.insert(0, _UI_DIR)
import streamlit as st
from styles import page_header_html
from constants import FOREST, SAND, RUST, SAGE, CREAM, WHITE, MIST, SCORE_EXCELLENT, SCORE_GOOD

def render():
    st.markdown(page_header_html("📊", "Results", "Review your performance and answers"), unsafe_allow_html=True)

    results_data = st.session_state.get("test_results")

    if not results_data:
        st.markdown(f"""
        <div style="background:{CREAM};border:1.5px solid {SAND}50;border-radius:14px;padding:28px;text-align:center;">
            <div style="font-size:36px;margin-bottom:10px;">📊</div>
            <div style="font-size:16px;font-weight:600;color:{FOREST};margin-bottom:6px;">No results yet</div>
            <div style="font-size:13.5px;color:{SAGE};">Complete a mock test first to see your results here.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🎯 Start Mock Test", use_container_width=True):
            st.session_state["current_page"] = "🎯 Mock Test"
            st.rerun()
        return

    pct      = results_data["percentage"]
    correct  = results_data["correct_count"]
    total    = results_data["num_questions"]
    results  = results_data["results"]
    cfg      = results_data.get("config", {})

    #Score header
    if pct >= SCORE_EXCELLENT:
        grade, color, emoji, label = "A", SAGE, "🏆", "Excellent!"
        card_class = "result-card-excellent"
    elif pct >= SCORE_GOOD:
        grade, color, emoji, label = "B", SAND, "👍", "Good Job!"
        card_class = "result-card-good"
    else:
        grade, color, emoji, label = "C", RUST, "📖", "Keep Practicing"
        card_class = "result-card-needs-work"

    st.markdown(f"""
    <div class="{card_class}" style="text-align:center;margin-bottom:20px;padding:28px;">
        <div style="font-size:44px;margin-bottom:8px;">{emoji}</div>
        <div style="font-family:'Playfair Display',serif;font-size:40px;font-weight:700;color:{color};">{pct:.0f}%</div>
        <div style="font-size:20px;font-weight:600;color:{FOREST};margin-top:4px;">{label}</div>
        <div style="font-size:14px;color:{SAGE};margin-top:6px;">{correct} of {total} questions correct</div>
        <div style="display:flex;gap:10px;justify-content:center;margin-top:12px;flex-wrap:wrap;">
            {"" if not cfg.get("difficulty") else f'<span style="font-size:12px;background:{SAND}25;color:{RUST};padding:3px 10px;border-radius:20px;font-weight:600;">{cfg.get("difficulty")}</span>'}
            {"" if not cfg.get("q_type") else f'<span style="font-size:12px;background:{SAGE}20;color:{SAGE};padding:3px 10px;border-radius:20px;font-weight:600;">{cfg.get("q_type")}</span>'}
        </div>
    </div>
    """, unsafe_allow_html=True)

    #Stats row 
    c1, c2, c3, c4 = st.columns(4)
    wrong  = total - correct - len([r for r in results if r.get("verdict") == "skipped"])
    skipped = len([r for r in results if r.get("verdict") == "skipped"])

    with c1:
        st.markdown(f"""<div style="background:{WHITE};border:1.5px solid {SAGE}40;border-radius:12px;padding:14px;text-align:center;">
            <div style="font-family:'Playfair Display',serif;font-size:26px;font-weight:700;color:{SAGE};">{correct}</div>
            <div style="font-size:11px;color:{SAGE};text-transform:uppercase;letter-spacing:0.8px;">Correct ✓</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div style="background:{WHITE};border:1.5px solid {RUST}40;border-radius:12px;padding:14px;text-align:center;">
            <div style="font-family:'Playfair Display',serif;font-size:26px;font-weight:700;color:{RUST};">{wrong}</div>
            <div style="font-size:11px;color:{RUST};text-transform:uppercase;letter-spacing:0.8px;">Wrong ✗</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div style="background:{WHITE};border:1.5px solid {SAND}40;border-radius:12px;padding:14px;text-align:center;">
            <div style="font-family:'Playfair Display',serif;font-size:26px;font-weight:700;color:{SAND};">{skipped}</div>
            <div style="font-size:11px;color:{SAND};text-transform:uppercase;letter-spacing:0.8px;">Skipped —</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        avg_sa = None
        sa_results = [r for r in results if r.get("type") in ("short_answer",)]
        if sa_results:
            avg_sa = sum(r.get("score", 0) for r in sa_results) / len(sa_results)
        val = f"{avg_sa:.1f}/10" if avg_sa is not None else f"{pct:.0f}%"
        st.markdown(f"""<div style="background:{WHITE};border:1.5px solid {FOREST}25;border-radius:12px;padding:14px;text-align:center;">
            <div style="font-family:'Playfair Display',serif;font-size:26px;font-weight:700;color:{FOREST};">{val}</div>
            <div style="font-size:11px;color:{FOREST};text-transform:uppercase;letter-spacing:0.8px;">Score</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    #Topic breakdown
    topics = {}
    for r in results:
        t = r.get("topic", "General")
        if not t:
            t = "General"
        if t not in topics:
            topics[t] = {"correct": 0, "total": 0}
        topics[t]["total"] += 1
        if r.get("verdict") == "correct" or r.get("score", 0) >= 7:
            topics[t]["correct"] += 1

    if len(topics) > 1:
        with st.expander("📈 Topic Breakdown", expanded=True):
            for topic, data in topics.items():
                t_pct = data["correct"] / data["total"] * 100 if data["total"] else 0
                col_t, col_p = st.columns([3, 1])
                with col_t:
                    st.markdown(f"<div style='font-size:13.5px;font-weight:500;color:{FOREST};margin-bottom:3px;'>{topic}</div>", unsafe_allow_html=True)
                    st.progress(t_pct / 100)
                with col_p:
                    c = SAGE if t_pct >= 70 else SAND if t_pct >= 50 else RUST
                    st.markdown(f"<div style='font-size:14px;font-weight:600;color:{c};padding-top:4px;'>{t_pct:.0f}%</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    #Detailed answers 
    st.markdown(f"""<div style="font-size:13px;font-weight:600;color:{SAGE};text-transform:uppercase;letter-spacing:1px;margin-bottom:12px;">Detailed Review</div>""", unsafe_allow_html=True)

    verdict_colors = {
        "correct":          (SAGE,  "✓ Correct",          "#F0F9F4"),
        "incorrect":        (RUST,  "✗ Incorrect",         "#FFF8F5"),
        "partially_correct":(SAND,  "~ Partial Credit",    CREAM),
        "skipped":          (MIST,  "— Skipped",           WHITE),
        "unknown":          (SAND,  "? Evaluated",         CREAM),
    }

    for i, r in enumerate(results):
        v = r.get("verdict", "unknown")
        vc, vl, bg = verdict_colors.get(v, (SAND, v, CREAM))
        score_disp = r.get("score", 0)

        with st.expander(f"Q{i+1}: {r.get('question', '')[:70]}{'…' if len(r.get('question',''))>70 else ''} — {vl}"):
            st.markdown(f"""
            <div style="background:{bg};border-radius:10px;padding:16px;margin-bottom:10px;">
                <div style="font-size:15px;font-weight:500;color:{FOREST};margin-bottom:12px;">{r.get('question','')}</div>

                <div style="margin-bottom:8px;">
                    <div style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.8px;color:{SAGE};margin-bottom:3px;">Your Answer</div>
                    <div style="font-size:14px;color:{FOREST};background:{WHITE};border:1px solid {SAND}30;border-radius:8px;padding:8px 12px;">{r.get('user_answer','(no answer)') or '(no answer)'}</div>
                </div>

                <div style="margin-bottom:8px;">
                    <div style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.8px;color:{SAGE};margin-bottom:3px;">Correct Answer</div>
                    <div style="font-size:14px;color:{SAGE};font-weight:500;background:{SAGE}12;border:1px solid {SAGE}30;border-radius:8px;padding:8px 12px;">{r.get('correct_answer','')}</div>
                </div>

                <div style="display:flex;align-items:center;gap:10px;margin-top:10px;">
                    <span style="font-size:12px;font-weight:700;background:{vc}20;color:{vc};padding:4px 12px;border-radius:20px;border:1px solid {vc}40;">{vl}</span>
                    <span style="font-size:12px;color:{SAGE};">{r.get('topic','')}</span>
                    {"" if r.get("type") not in ("short_answer",) else f'<span style="font-size:12px;color:{vc};font-weight:600;">Score: {score_disp}/10</span>'}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if r.get("feedback") and r.get("feedback") not in ("✓ Correct!",):
                st.markdown(f"""
                <div style="background:{WHITE};border-left:3px solid {vc};border-radius:0 8px 8px 0;padding:10px 14px;font-size:13.5px;color:{FOREST};margin-bottom:8px;">
                    <b>Feedback:</b> {r.get('feedback','')}
                </div>
                """, unsafe_allow_html=True)

            missed = r.get("missed_points", [])
            if missed:
                st.markdown(f"<div style='font-size:13px;color:{RUST};font-weight:600;margin-top:6px;'>Points missed:</div>", unsafe_allow_html=True)
                for pt in missed:
                    st.markdown(f"- {pt}")

    #Actions
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Retake Test", use_container_width=True):
            st.session_state["mock_submitted"] = False
            st.session_state["mock_answers"]   = {}
            st.session_state["current_page"]   = "🎯 Mock Test"
            st.rerun()
    with col2:
        if st.button("⚙️ New Test Config", use_container_width=True):
            st.session_state["mock_questions"] = []
            st.session_state["current_page"]   = "🎯 Mock Test"
            st.rerun()
    with col3:
        if st.button("💬 Chat About Results", use_container_width=True):
            # Pre-load a context message
            summary = f"I just scored {pct:.0f}% ({correct}/{total}) on a {cfg.get('difficulty','')} test."
            st.session_state["pending_chat"] = f"{summary} What topics should I focus on to improve?"
            st.session_state["current_page"] = "💬 AI Chat"
            st.rerun()
