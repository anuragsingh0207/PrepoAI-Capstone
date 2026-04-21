"""
rag_engine.py
Responsibility: Core RAG engine connecting Vector DB to LLM via LangChain.
"""
import os
import sys

# Ensure config is accessible
try:
    import config
except ImportError:
    pass

from langchain_groq import ChatGroq
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank

from backend.prompts import SYSTEM_PROMPT

def get_rag_chain(vector_store):
    """
    Creates a conversational RAG chain.
    """
    try:
        import config
        llm_model = getattr(config, "LLM_MODEL", "llama-3.3-70b-versatile")
        llm_temp = getattr(config, "LLM_TEMP", 0.3)
        rerank_n = getattr(config, "TOP_N_RERANK", 5)
        retrieval_k = getattr(config, "RETRIEVAL_K", 20)
    except:
        llm_model = "llama-3.3-70b-versatile"
        llm_temp = 0.3
        rerank_n = 5
        retrieval_k = 20

    llm = ChatGroq(model=llm_model, temperature=llm_temp)
    
    # 1. Retriever Setup
    base_retriever = vector_store.as_retriever(search_kwargs={"k": retrieval_k}) 
    
    if os.getenv("COHERE_API_KEY"):
        print("Cohere Reranking Enabled")
        compressor = CohereRerank(model="rerank-english-v3.0", top_n=rerank_n)
        retriever = ContextualCompressionRetriever(
            base_compressor=compressor, base_retriever=base_retriever
        )
    else:
        print("Cohere Reranking Disabled (Key not found)")
        retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    # 2. History Aware Retriever
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

def generate_response(rag_chain, prompt):
    """
    Executes the LLM generation securely with the constructed prompt.
    """
    return rag_chain.invoke({
        "input": prompt,
        "chat_history": []
    })

