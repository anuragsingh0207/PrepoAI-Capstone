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

from backend.prompts import SYSTEM_PROMPT, build_dynamic_prompt
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

    from dotenv import load_dotenv
    load_dotenv()

    llm = ChatGroq(
    model=llm_model,
    temperature=llm_temp,
    api_key=os.getenv("GROQ_API_KEY")
)

    
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


    # 3. QA Chain (Generation – dynamic prompt)
    # Collect dynamic tool mode and config if provided
    selected_tool = getattr(config, "SELECTED_TOOL", "qpaper")
    tool_config = getattr(config, "TOOL_CONFIG", {})

    user_mode_prompt = build_dynamic_prompt(selected_tool, tool_config)
    combined_prompt = SYSTEM_PROMPT + "\n\n" + user_mode_prompt + "\n\nContext:\n{context}"

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", combined_prompt),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    return rag_chain

from streamlit import session_state as st
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


def get_message_history(session_id: str = "default"):
    """Maintain per‑session chat history."""
    if "chat_histories" not in st:
        st.chat_histories = {}
    if session_id not in st.chat_histories:
        st.chat_histories[session_id] = ChatMessageHistory()
    return st.chat_histories[session_id]


def generate_response_with_sources(rag_chain, prompt):
    """
    Executes RAG and returns both the answer and metadata‑based sources.
    Keeps chat history persistent across questions.
    """
    history = get_message_history("default")
    rag_with_memory = RunnableWithMessageHistory(
        rag_chain,
        get_message_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    result = rag_with_memory.invoke(
        {"input": prompt}, config={"configurable": {"session_id": "default"}}
    )

    answer = result.get("answer", result)
    context_docs = result.get("context", [])
    sources = []

    for d in context_docs:
        meta = d.metadata
        src = meta.get("source", "Unknown")
        page = meta.get("page") or meta.get("slide")
        if page:
            sources.append(f"{src} (p.{page})")
        else:
            sources.append(src)

    return answer, list(set(sources))
