import sys, os as _os
_UI_DIR = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), ".."))
if _UI_DIR not in sys.path:
    sys.path.insert(0, _UI_DIR)
import streamlit as st
from styles import page_header_html
from config import get_gemini_client, evaluate_answer
from constants import FOREST, SAND, RUST, SAGE, CREAM, WHITE, PAGE_RESULT, PAGE_MOCK

def render():
    st.markdown(page_header_html("🎯", "Mock Test", "Answer the questions — take your time"), unsafe_allow_html=True)

    questions = st.session_state.get("mock_questions", [])
    submitted = st.session_state.get("mock_submitted", False)

    if not questions:
        st.markdown(f"""
        <div style="background:{CREAM};border:1.5px solid {SAND}50;border-radius:14px;padding:28px;text-align:center;">
            <div style="font-size:36px;margin-bottom:10px;">🎯</div>
            <div style="font-size:16px;font-weight:600;color:{FOREST};margin-bottom:6px;">No test configured</div>
            <div style="font-size:13.5px;color:{SAGE};">Go to Mock Test → Configure & Start to generate questions.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⚙️ Configure Test", use_container_width=True):
            st.session_state["current_page"] = "🎯 Mock Test"
            st.rerun()
        return

    cfg = st.session_state.get("mock_config", {})
    answers = st.session_state.get("mock_answers", {})

    #Progress bar 
    answered = len([k for k, v in answers.items() if v is not None and v != ""])
    progress = answered / len(questions) if questions else 0
    st.markdown(f"""
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;">
        <div style="font-size:13px;font-weight:500;color:{SAGE};">Progress: {answered}/{len(questions)} answered</div>
        <div style="display:flex;gap:8px;">
            <span style="font-size:12px;background:{SAND}25;color:{RUST};padding:3px 10px;border-radius:20px;font-weight:600;">{cfg.get('difficulty','')}</span>
            <span style="font-size:12px;background:{SAGE}20;color:{SAGE};padding:3px 10px;border-radius:20px;font-weight:600;">{cfg.get('q_type','')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(progress)
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    #Questions 
    for i, q in enumerate(questions):
        qid    = q.get("id", i + 1)
        qtype  = q.get("type", "mcq").lower()
        qtext  = q.get("question", "")
        opts   = q.get("options", [])
        topic  = q.get("topic", "")

        st.markdown(f"""
        <div class="question-card">
            <div class="q-number">Question {i+1} of {len(questions)}{' · '+topic if topic else ''}</div>
            <div class="q-text">{qtext}</div>
            {"" if not topic else ""}
        </div>
        """, unsafe_allow_html=True)

        key = f"ans_{qid}"

        if qtype in ("mcq", "multiple_choice") and opts:
            ans = st.radio(
                f"Select answer for Q{i+1}",
                opts,
                key=key,
                label_visibility="collapsed",
                index=None if key not in st.session_state else None,
            )
            answers[qid] = ans

        elif qtype in ("true_false", "true/false"):
            ans = st.radio(
                f"Select for Q{i+1}",
                ["True", "False"],
                key=key,
                label_visibility="collapsed",
                index=None,
            )
            answers[qid] = ans

        elif qtype in ("short_answer", "short answer"):
            ans = st.text_area(
                f"Your answer for Q{i+1}",
                key=key,
                placeholder="Type your answer here…",
                height=100,
                label_visibility="collapsed",
            )
            answers[qid] = ans

        else:
            # Default MCQ fallback
            if opts:
                ans = st.radio(f"Q{i+1}", opts, key=key, label_visibility="collapsed", index=None)
                answers[qid] = ans
            else:
                ans = st.text_area(f"Your answer for Q{i+1}", key=key, height=100, label_visibility="collapsed")
                answers[qid] = ans

        st.session_state["mock_answers"] = answers
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    #Submit
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    unanswered = len(questions) - len([v for v in answers.values() if v is not None and v != ""])
    if unanswered > 0:
        st.warning(f"⚠️ {unanswered} question(s) unanswered. You can still submit.")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Submit Test", use_container_width=True, type="primary"):
            with st.spinner("Evaluating your answers…"):
                _evaluate_and_save(questions, answers)
            st.session_state["mock_submitted"] = True
            st.session_state["current_page"] = PAGE_RESULT
            st.rerun()

    if st.button("🔄 Restart Test", use_container_width=True):
        st.session_state["mock_questions"] = []
        st.session_state["mock_answers"]   = {}
        st.session_state["mock_submitted"] = False
        st.rerun()


def _evaluate_and_save(questions: list[dict], answers: dict):
    client = get_gemini_client()
    results = []
    total_score = 0
    max_score   = 0

    for q in questions:
        qid     = q.get("id", 0)
        qtype   = q.get("type", "mcq").lower()
        correct = q.get("correct_answer", "")
        user_a  = answers.get(qid, "")
        max_score += 10

        if not user_a:
            results.append({
                "question": q.get("question"),
                "user_answer": "(No answer)",
                "correct_answer": correct,
                "type": qtype,
                "score": 0,
                "verdict": "skipped",
                "feedback": "No answer provided.",
                "missed_points": [],
                "strong_points": [],
                "topic": q.get("topic", ""),
                "options": q.get("options", []),
            })
            continue

        if qtype in ("mcq", "multiple_choice", "true_false", "true/false"):
            # Exact match (compare stripped lowercase)
            def _norm(s):
                s = str(s).strip().lower()
                # strip leading "a. ", "b. " etc
                import re
                s = re.sub(r'^[a-d]\.\s*', '', s)
                return s
            correct_n = _norm(correct)
            user_n    = _norm(user_a)
            is_correct = correct_n == user_n or str(correct).strip().lower() in str(user_a).strip().lower()
            score    = 10 if is_correct else 0
            verdict  = "correct" if is_correct else "incorrect"
            feedback = "✓ Correct!" if is_correct else f"The correct answer was: {correct}"
        else:
            # Short answer: use AI evaluation
            eval_result = evaluate_answer(client, q.get("question"), correct, user_a)
            score   = eval_result.get("score", 5)
            verdict = eval_result.get("verdict", "unknown")
            feedback = eval_result.get("feedback", "")
            eval_result["question"]       = q.get("question")
            eval_result["user_answer"]    = user_a
            eval_result["correct_answer"] = correct
            eval_result["type"]           = qtype
            eval_result["topic"]          = q.get("topic", "")
            eval_result["options"]        = q.get("options", [])
            results.append(eval_result)
            total_score += score
            continue

        total_score += score
        results.append({
            "question": q.get("question"),
            "user_answer": user_a,
            "correct_answer": correct,
            "type": qtype,
            "score": score,
            "verdict": verdict,
            "feedback": feedback,
            "missed_points": [],
            "strong_points": [],
            "topic": q.get("topic", ""),
            "options": q.get("options", []),
        })

    percentage = (total_score / max_score * 100) if max_score else 0

    st.session_state["test_results"] = {
        "results": results,
        "total_score": total_score,
        "max_score": max_score,
        "percentage": percentage,
        "num_questions": len(questions),
        "correct_count": len([r for r in results if r.get("verdict") == "correct"]),
        "config": st.session_state.get("mock_config", {}),
    }

    # Update global stats
    if "stats" not in st.session_state:
        st.session_state.stats = {}
    stats = st.session_state.stats
    stats["tests_taken"] = stats.get("tests_taken", 0) + 1
    stats["questions_answered"] = stats.get("questions_answered", 0) + len(questions)
    all_scores = stats.get("all_scores", [])
    all_scores.append(percentage)
    stats["all_scores"] = all_scores
    stats["avg_score"]  = sum(all_scores) / len(all_scores)
