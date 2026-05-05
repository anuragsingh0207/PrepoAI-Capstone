# PrepoAI: Intelligent Educational RAG System

### Capstone Project - BS CSDA (IIT Patna)

## 👥 Team
- **Anurag Singh** – Project Lead, System Design
- **Anshika Singh** – RAG System, LLM Integration, AI Features

---


## 🧠 My Contribution (Anshika Singh)

- Built the **RAG pipeline** (ingestion → retrieval → LLM response)
- Implemented **FAISS-based contextual retrieval**
- Integrated **LLM APIs (Groq)** with prompt engineering
- Designed **multi-mode system** (QGen, Summary, Flashcards, Evaluation)
- Added **conversation memory (history-aware chat)**
- Implemented **answer evaluation + source citation**

> Note: This was a collaborative project. Contributions listed reflect primary areas of responsibility.  

**Tech Stack:** Python, LangChain, Groq API, Cohere, FAISS, Streamlit

---

## 📌 Project Overview

PrepoAI is a Retrieval-Augmented Generation (RAG) system designed to process unstructured educational data (PDFs, lecture notes, slides). It leverages **vector search + LLM reasoning** to create an interactive AI-powered study assistant.

The system enables users to upload study material and interact with it through multiple intelligent modes like question generation, summaries, flashcards, and answer evaluation.

---

## 🚀 Key Features

### 🧠 RAG Intelligence Layer (Implemented by Anshika Singh)

* **Metadata-Aware Ingestion** (source, page/slide tracking)
* **Contextual Retrieval (FAISS + optional reranking)**
* **Conversational Memory (history-aware RAG)**
* **Multi-Mode Prompt System:**

  * 📝 Question Paper Generation
  * 🧾 Summary Mode
  * 🃏 Flashcards
  * 🧠 Answer Evaluation (grading + feedback)
* **Source Citation System** for explainability

---

### 📄 Data Processing

* Extracts and cleans text from PDFs, PPTs, and documents
* Structure-aware chunking for better retrieval accuracy

---

### 💬 Interactive UI

* Streamlit-based multi-view interface
* Chat-based document querying
* Mock test environment with evaluation
* Configurable generation (difficulty, question types, etc.)

---

## 📂 Module Breakdown

* **Data Pipeline:** `backend/ingestion.py`
* **Vector Store:** `backend/embeddings.py`
* **RAG Engine:** `backend/rag_engine.py`
* **Prompt Logic:** `backend/prompts.py`
* **Frontend UI:** `src/app.py` + `ui/views/`

---

## 🛠️ Installation

1. Clone the repo:

```bash
git clone https://github.com/anuragsingh0207/PrepoAI-Capstone.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create `.env` file:

```env
GROQ_API_KEY=your_key_here
COHERE_API_KEY=your_key_here (optional)
```

4. Run the app:

```bash
streamlit run src/app.py
```

---

## 🎯 Future Enhancements

* Hybrid Retrieval (BM25 + Vector Search)
* Knowledge Graph / Mindmap generation
* Improved UI/UX polish
* Performance optimization & caching

---

## 📌 Note

This project demonstrates a complete **end-to-end RAG system with memory, evaluation, and multi-mode interaction**, going beyond basic document Q&A systems.
