"""
config.py
Responsibility: Environment loading and core configuration properties
"""
import os
from dotenv import load_dotenv

# Apply environment loaded globally upon the first import of this config
load_dotenv()

# System Config
LLM_MODEL = "llama-3.3-70b-versatile"
LLM_TEMP = 0.3
EMBED_MODEL = "embed-english-v3.0"
RERANK_MODEL = "rerank-english-v3.0"
TOP_N_RERANK = 5
RETRIEVAL_K = 20
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Validations
if not os.getenv("GROQ_API_KEY") and not os.getenv("GOOGLE_API_KEY"):
    pass # No severe crash here, wait until runtime to let LLM lib complain or handle explicitly

