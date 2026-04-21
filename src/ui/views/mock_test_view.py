import streamlit as st
import time
from backend.prompts import build_dynamic_prompt, build_eval_prompt
from backend.rag_engine import generate_response

def render():
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Finish / Exit", key="mt_exit"):
            if st.session_state.get('mock_questions'):
                st.session_state.current_view = 'RESULT'
            else:
                st.session_state.current_view = 'ACTION'
                st.session_state.mock_test_active = False
            st.rerun()

    st.markdown("### Mock Test Mode")
    
    # ---------------------------------------------------------
    # Setup Phase
    # ---------------------------------------------------------
    if not st.session_state.get('mock_test_active', False):
        st.caption("A dedicated, timed focus environment.")
        rounds = st.number_input("Total Questions", min_value=1, max_value=20, value=5)
        mt_type = st.selectbox("Test Type", ["Technical", "Conceptual", "Mixed"])
        
        if st.button("Start Timer & Test", type="primary"):
            prompt = build_dynamic_prompt('interview', {"duration": rounds, "round_type": mt_type})
            with st.spinner("Generating Test Scenario..."):
                response = generate_response(st.session_state.rag_chain, prompt)
                raw_text = response["answer"]
                
                # Parse questions securely
                questions = [q.strip() for q in raw_text.split("|||") if q.strip()]
                # Fallback if LLM ignores delimiter formatting
                if len(questions) == 1:
                    questions = [q.strip() for q in raw_text.split("\n\n") if q.strip()]
                
                # Initialize States
                st.session_state.mock_questions = questions
                st.session_state.mock_answers = [""] * len(questions)
                st.session_state.mock_evaluations = [None] * len(questions)
                st.session_state.mock_current_q = 0
                st.session_state.mock_test_start_time = time.time()
                st.session_state.mock_test_active = True
                
            st.rerun()
            
    # ---------------------------------------------------------
    # Active Test Phase
    # ---------------------------------------------------------
    else:
        # 1. Timer Logic
        elapsed = int(time.time() - st.session_state.mock_test_start_time)
        mins, secs = divmod(elapsed, 60)
        
        st.markdown(f"""
        <div style="background:#1a3a2a; padding:10px; border-radius:8px; border:1px solid #4cd964; margin-bottom:1rem; text-align:center;">
             <span style="color:#4cd964; font-family:'JetBrains Mono', monospace; font-size:18px; font-weight:600;">⏱️ TIME ELAPSED: {mins:02d}:{secs:02d}</span>
        </div>
        """, unsafe_allow_html=True)
        
        q_idx = st.session_state.mock_current_q
        total_q = len(st.session_state.mock_questions)
        current_question = st.session_state.mock_questions[q_idx]
        
        st.markdown(f"**Question {q_idx + 1} of {total_q}**")
        st.info(current_question)
        
        # 2. Answer Input
        answer_text = st.text_area(
            "Your Answer", 
            value=st.session_state.mock_answers[q_idx], 
            height=200, 
            key=f"ans_input_{q_idx}"
        )
        
        # 3. Action Buttons (Submit, Navigate)
        cA, cB, cC = st.columns(3)
        with cA:
            if st.button("Submit & Evaluate", type="primary", use_container_width=True):
                # Save answer
                st.session_state.mock_answers[q_idx] = answer_text
                
                if answer_text.strip():
                    eval_prompt = build_eval_prompt(current_question, answer_text, max_marks=10)
                    with st.spinner("Evaluating your response..."):
                        try:
                            eval_resp = generate_response(st.session_state.rag_chain, eval_prompt)
                            st.session_state.mock_evaluations[q_idx] = eval_resp["answer"]
                        except Exception as e:
                            st.error(f"Failed to evaluate: {e}")
                else:
                    st.warning("Please write an answer before evaluating.")
                    
        with cB:
            if st.button("⬅️ Previous", disabled=(q_idx == 0), use_container_width=True):
                st.session_state.mock_answers[q_idx] = answer_text
                st.session_state.mock_current_q -= 1
                st.rerun()
                
        with cC:
            if st.button("Skip / Next ➡️", disabled=(q_idx == total_q - 1), use_container_width=True):
                st.session_state.mock_answers[q_idx] = answer_text
                st.session_state.mock_current_q += 1
                st.rerun()
                
        # 4. Display Evaluation if it exists
        if st.session_state.mock_evaluations[q_idx]:
            st.markdown("---")
            st.markdown("### 🎓 Teacher's Evaluation")
            st.markdown(f"<div style='background:#1e1e1c; padding:15px; border-radius:10px; border:1px solid #333;'>{st.session_state.mock_evaluations[q_idx]}</div>", unsafe_allow_html=True)
