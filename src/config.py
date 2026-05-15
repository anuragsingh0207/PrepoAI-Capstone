import streamlit as st
from google import genai
from google.genai import types
import json, re
from constants import (
    GEMINI_MODEL, CHAT_SYSTEM_PROMPT,
    QUESTION_SYSTEM_PROMPT, EVALUATION_SYSTEM_PROMPT,
    DEFAULT_TEMPERATURE, DEFAULT_MAX_TOKENS
)

API_KEY = ""

@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=API_KEY)

def build_context_from_docs(uploaded_docs: list[dict]) -> str:
    """Combine all uploaded document texts into a single context string."""
    if not uploaded_docs:
        return ""
    parts = []
    for doc in uploaded_docs:
        parts.append(f"--- Document: {doc['name']} ---\n{doc['text']}\n")
    return "\n".join(parts)

def stream_chat_response(client, messages: list[dict], context: str):
    """Stream a chat response from Gemini with document context."""
    system = CHAT_SYSTEM_PROMPT
    if context:
        system += f"\n\nStudy Material provided by user:\n{context}"

    contents = []
    for m in messages:
        role = "user" if m["role"] == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part(text=m["content"])]))

    config = types.GenerateContentConfig(
        system_instruction=system,
        temperature=st.session_state.get("temperature", DEFAULT_TEMPERATURE),
        max_output_tokens=st.session_state.get("max_tokens", DEFAULT_MAX_TOKENS),
    )
    response = client.models.generate_content_stream(
        model=GEMINI_MODEL, contents=contents, config=config
    )
    for chunk in response:
        if chunk.text:
            yield chunk.text

def generate_questions(client, context: str, num_q: int, difficulty: str, q_type: str) -> list[dict]:
    """Call Gemini to generate quiz questions from context."""
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

    contents = [
        types.Content(role="user", parts=[
            types.Part(text=f"Study material:\n{context[:12000]}\n\nGenerate {num_q} questions now.")
        ])
    ]
    config = types.GenerateContentConfig(
        system_instruction=prompt_template,
        temperature=0.8,
        max_output_tokens=3000,
    )
    response = client.models.generate_content(
        model=GEMINI_MODEL, contents=contents, config=config
    )
    raw = response.text.strip()
    # Strip markdown code fences if present
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    try:
        data = json.loads(raw)
        return data.get("questions", [])
    except Exception:
        return []

def evaluate_answer(client, question: str, correct_answer: str, user_answer: str) -> dict:
    """Evaluate a user's answer for short-answer questions."""
    contents = [
        types.Content(role="user", parts=[
            types.Part(text=(
                f"Question: {question}\n"
                f"Correct answer: {correct_answer}\n"
                f"Student's answer: {user_answer}\n"
                f"Evaluate now."
            ))
        ])
    ]
    config = types.GenerateContentConfig(
        system_instruction=EVALUATION_SYSTEM_PROMPT,
        temperature=0.3,
        max_output_tokens=500,
    )
    response = client.models.generate_content(
        model=GEMINI_MODEL, contents=contents, config=config
    )
    raw = response.text.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    try:
        return json.loads(raw)
    except Exception:
        return {"score": 5, "verdict": "unknown", "feedback": raw, "missed_points": [], "strong_points": []}
