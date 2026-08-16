# PrepoAI - Intelligent Educational RAG System

PrepoAI is an advanced educational study assistant built with Streamlit, LangChain, FAISS, and Groq. It allows students to upload their study materials (PDF, DOCX, TXT) and instantly generate varying depths of summaries, complex interactive mock tests, and chat contextually with their documents.

## Project Architecture
- **Frontend & Routing:** Streamlit (`src/app.py` -> `src/ui/views/`)
- **Backend Orchestration:** LangChain
- **Vector Database:** FAISS (Local CPU implementation)
- **Embeddings:** HuggingFace `sentence-transformers`
- **LLM Engine:** Groq API (`llama-3.3-70b-versatile`)
- **Document Parsing:** PyPDF, python-docx

## Local Installation

### 1. Prerequisites
- Python 3.10+
- Git
- Valid Groq API Key (Get yours at [Groq Console](https://console.groq.com/keys))

### 2. Clone the Repository
```bash
git clone https://github.com/anuragsingh0207/PrepoAI-Capstone.git
cd PrepoAI-Capstone
```

### 3. Create a Virtual Environment
**Windows:**
```bash
python -m venv prepoai-venv
prepoai-venv\Scripts\activate
```
**macOS/Linux:**
```bash
python3 -m venv prepoai-venv
source prepoai-venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Copy the example environment file and add your API keys:
```bash
cp .env.example .env
```
Open `.env` and fill in `GROQ_API_KEY`.

### 6. Run the Application
```bash
streamlit run src/app.py
```
Your browser will automatically open to `http://localhost:8501`.

---

## Deployment (Render / Streamlit Cloud)

> **⚠️ Important Deployment Note:** The current architecture uses Streamlit (stateful WebSockets) and FAISS + HuggingFace (large model downloads & persistent in-memory database). **It is NOT compatible with Vercel Serverless Functions.**

We highly recommend deploying to **Render** or **Streamlit Community Cloud** which natively support long-running stateful Python applications.

### Option A: Streamlit Community Cloud (Easiest)
1. Push your repository to GitHub.
2. Sign up at [share.streamlit.io](https://share.streamlit.io/).
3. Click **New app** and select your repository, branch, and `src/app.py` as the main file path.
4. Go to **Advanced settings** and paste the contents of your `.env` file into the "Secrets" box.
5. Click **Deploy!**

### Option B: Render Web Service (More Control)
1. Create a new "Web Service" on [Render](https://render.com/).
2. Connect your GitHub repository.
3. Use the following settings:
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run src/app.py --server.port $PORT`
4. Go to **Environment Variables** and add your `GROQ_API_KEY`.
5. Click **Create Web Service**.

## Troubleshooting
- **ModuleNotFoundError: No module named 'pypdf'**: Ensure you ran `pip install -r requirements.txt` inside your activated virtual environment.
- **GROQ_API_KEY missing**: Make sure your `.env` file is in the root directory and properly formatted.
- **Out of Memory on Deployment**: FAISS and HuggingFace models consume ~500MB RAM. Ensure your deployment tier has at least 1GB of RAM.

## Technical Debt / Known Issues
- `src/backend/ingestion.py` and `src/backend/rag_engine.py` are currently bypassing the actual execution flow in favor of an optimized UI-first logic found in `src/ui/views/workspace_view.py`. They remain for future API decouplings.
