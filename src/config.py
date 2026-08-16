import streamlit as st
from groq import Groq
import json, re
import os
from dotenv import load_dotenv
from constants import (
    GROQ_MODEL, CHAT_SYSTEM_PROMPT,
    QUESTION_SYSTEM_PROMPT, EVALUATION_SYSTEM_PROMPT,
    DEFAULT_TEMPERATURE, DEFAULT_MAX_TOKENS
)

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY", "")

@st.cache_resource
def get_groq_client():
    return Groq(api_key=API_KEY)

def build_context_from_docs(uploaded_docs: list[dict]) -> str:
    if not uploaded_docs:
        return ""
    parts = []
    for doc in uploaded_docs:
        parts.append(f"--- Document: {doc['name']} ---\n{doc['text']}\n")
    return "\n".join(parts)

def stream_chat_response(client, messages: list[dict], context: str):
    system = CHAT_SYSTEM_PROMPT
    if context:
        system += f"\n\nStudy Material provided by user:\n{context}"

    groq_messages = [{"role": "system", "content": system}]
    for m in messages:
        groq_messages.append({"role": m["role"], "content": m["content"]})

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=groq_messages,
        temperature=st.session_state.get("temperature", DEFAULT_TEMPERATURE),
        max_tokens=st.session_state.get("max_tokens", DEFAULT_MAX_TOKENS),
        stream=True
    )
    for chunk in response:
        text = chunk.choices[0].delta.content
        if text:
            yield text

def generate_questions(client, context: str, num_q: int, difficulty: str, q_type: str) -> list[dict]:
    if not context:
        return []

    type_map = {"MCQ": "mcq", "Short Answer": "short_answer",
                "True/False": "true_false", "Mixed": "mixed"}
    q_type_key = type_map.get(q_type, "mcq")

    prompt_template = QUESTION_SYSTEM_PROMPT.format(
        num_questions=num_q,
        difficulty=difficulty.lower(),
        question_type=q_type_key
    )

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": prompt_template},
            {"role": "user", "content": f"Study material:\n{context[:12000]}\n\nGenerate {num_q} questions now."}
        ],
        temperature=0.8,
        max_tokens=3000,
        stream=False
    )
    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    try:
        data = json.loads(raw)
        return data.get("questions", [])
    except Exception:
        return []

def evaluate_answer(client, question: str, correct_answer: str, user_answer: str) -> dict:
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": EVALUATION_SYSTEM_PROMPT},
            {"role": "user", "content": (
                f"Question: {question}\n"
                f"Correct answer: {correct_answer}\n"
                f"Student's answer: {user_answer}\n"
                f"Evaluate now."
            )}
        ],
        temperature=0.3,
        max_tokens=500,
        stream=False
    )
    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    try:
        return json.loads(raw)
    except Exception:
        return {"score": 5, "verdict": "unknown", "feedback": raw, "missed_points": [], "strong_points": []}