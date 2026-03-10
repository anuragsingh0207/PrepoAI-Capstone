"""
rag_engine.py
Responsibility: Anshika

This module acts as the core RAG engine, integrating the Vector Database with the LLM (Google Gemini) to provide context-aware answers.
It includes optional Cohere Reranking for improved accuracy and supports conversational history.
"""
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank

load_dotenv()

# The meticulous "Expert Academic Tutor" prompt provided by the user
SYSTEM_PROMPT = """You are an expert academic tutor and exam coach.

Objective:
Given retrieved context from student-uploaded documents (textbooks, notes, slides, PDFs), generate the most likely, high-quality exam-oriented practice questions that maximize scoring potential and conceptual mastery.

Context Handling Rules (RAG-Aware):

You will receive retrieved chunks of text from a vector database.

Treat the retrieved content as the only trusted source of truth.

Do NOT hallucinate beyond the provided context.

If the retrieved content is insufficient, explicitly say:
“The uploaded material does not contain enough information to generate meaningful exam questions.”

Question Generation Guidelines:
From the provided content, generate:

High-Probability Exam Questions

Focus on topics that are:

Repeated

Definition-heavy

Formula-based

Theoretical explanations

Diagrams/process flows

Comparisons

Derivations

Prioritize questions that teachers commonly ask.

Multiple Difficulty Levels

Easy: Direct recall / definitions

Medium: Concept application

Hard: Derivations, explanations, case-based or mixed-topic questions

Exam-Oriented Formats

Short Answer

Long Answer

Numerical / Derivation (if applicable)

MCQs (optional if content supports it)

Output Structure (STRICT FORMAT):

📘 Important Exam Questions from Your Notes

🔹 Very Important (High Probability)
1. ...
2. ...

🔹 Medium Importance
1. ...
2. ...

🔹 Conceptual / Tricky
1. ...
2. ...

🔹 Quick Revision Questions
1. ...
2. ...


Smart Emphasis

Bold important terms

Highlight formulas

Mention diagrams if helpful

Combine related concepts into single high-yield questions

No Fluff Policy

Do NOT add motivational lines

Do NOT explain what RAG is

Do NOT talk about the system

Do NOT add generic study advice

Accuracy Constraint

Every question must be traceable to the retrieved content.

If a topic is missing in context, do not invent questions for it.

You must prioritize exam relevance over completeness. If forced to choose, generate fewer high-quality, exam-focused questions rather than many low-quality generic ones. Optimize for marks, not coverage.

Predict which questions have the highest probability of appearing in exams based on patterns like definitions, contrasts, steps, advantages/disadvantages, and derivations. Rank questions accordingly.
"""

def get_rag_chain(vector_store):
    """
    Creates a conversational RAG chain.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-flash-latest", temperature=0.3)
    
    # 1. Retriever Setup
    base_retriever = vector_store.as_retriever(search_kwargs={"k": 20}) # Retrieve more docs initially for reranking
    
    # Check for Cohere API Key for Reranking
    if os.getenv("COHERE_API_KEY"):
        print("Cohere Reranking Enabled")
        compressor = CohereRerank(model="rerank-english-v3.0", top_n=5) # Re-rank to get top 5 best chunks
        retriever = ContextualCompressionRetriever(
            base_compressor=compressor, base_retriever=base_retriever
        )
    else:
        print("Cohere Reranking Disabled (Key not found)")
        retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    # 2. History Aware Retriever (to rephrase questions based on chat history)
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )
    
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
        ]
    )
    
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    # 3. QA Chain (Generation)
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT + "\n\nContext:\n{context}"),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
        ]
    )
    
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    
    return rag_chain

if __name__ == "__main__":
    print("Run from app.py")
