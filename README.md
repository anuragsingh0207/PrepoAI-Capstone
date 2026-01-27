# PrepoAI: Intelligent Educational RAG System
### Capstone Project - BS CSDA (IIT Patna)

**Project Lead:** Anurag
**Tech Stack:** Python, LangChain, Gemini API, ChromaDB, Streamlit.

## 📌 Project Overview
PrepoAI is a Retrieval-Augmented Generation (RAG) system designed to process unstructured educational data (PDFs, Lecture Notes). It utilizes **Vector Space Modeling** to index content and provides an interactive "Study Companion" interface for students.

## 🚀 Key Features
- **Automated Ingestion:** Extracts and cleans text from raw PDF documents.
- **Vector Search:** Uses Cosine Similarity to retrieve context-aware answers.
- **Generative AI:** Integrated with Google Gemini for natural language explanations.
- **Quiz Mode:** (Coming Soon) Auto-generates assessments based on uploaded content.

## 📂 Module Breakdown
- **Data Pipeline:** `src/ingestion.py` (Text Extraction)
- **Vector Database:** `src/embeddings.py` (Embedding Generation)
- **AI Logic:** `src/rag_engine.py` (LLM Integration)
- **Frontend:** `src/app.py` (User Interface)

## 🛠️ Installation
1. Clone the repo:
   ```bash
   git clone https://github.com/anuragsingh0207/PrepoAI-Capstone.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run src/app.py
   ```
