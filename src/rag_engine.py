"""
LLM Integration Module
Responsible for generating answers using an LLM given
a user query and retrieved context chunks.
"""

import os
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "models/gemini-pro"


def build_prompt(query: str, context_chunks: list[str]) -> str:
    """
    Build a RAG-style prompt using retrieved context.
    """
    context = "\n\n".join(context_chunks)

    prompt = f"""
You are a helpful study assistant.
Answer the question strictly using the provided context.
If the answer is not contained in the context, say "I don't know."

Context:
{context}

Question:
{query}

Answer:
"""
    return prompt.strip()


def generate_answer(query: str, context_chunks: list[str]) -> str:
    """
    Generate an answer for the given query using Gemini.
    """
    prompt = build_prompt(query, context_chunks)

    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)

    return response.text.strip()
