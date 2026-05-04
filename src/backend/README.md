# Backend Module

**Purpose**: Strictly houses the functional intelligence layer of PrepoAI, implementing a Retrieval-Augmented Generation (RAG) system with conversational memory and multi-mode capabilities.

**Contents**:

* `ingestion.py`: Handles document parsing (PDF, PPTX, etc.), performs file-level chunking, and attaches metadata (source, page/slide) to each chunk for accurate retrieval and citation.
* `embeddings.py`: Generates vector embeddings and stores them using FAISS for efficient similarity search (supports Cohere/HuggingFace models).
* `rag_engine.py`: Implements a LangChain-based, history-aware conversational RAG pipeline with chat memory, contextual retrieval, optional reranking, and source attribution.
* `prompts.py`: Defines structured prompt templates and dynamic prompt builders for multiple modes (question paper, summary, flashcards, evaluation), ensuring controlled and consistent LLM outputs.

**Key Capabilities**:

* Multi-mode response generation (questions, summaries, flashcards, evaluation)
* Context-aware retrieval with metadata grounding
* Conversational memory across interactions
* Transparent outputs with source citations
