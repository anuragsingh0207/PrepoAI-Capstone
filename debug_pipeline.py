"""
PrepoAI Full Pipeline Diagnostic Script
Run with: python debug_pipeline.py
"""
import os, sys, json, traceback, io

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
sys.path.insert(0, SRC_DIR)

from dotenv import load_dotenv
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

SEPARATOR = "=" * 60

def section(title):
    print(f"\n{SEPARATOR}\n{title}\n{SEPARATOR}")

# ─────────────────────────────────────────────────────────────
# PHASE 1 — ENV & API KEY
# ─────────────────────────────────────────────────────────────
section("PHASE 1: Environment & API Keys")

api_key = os.getenv("GROQ_API_KEY", "")
cohere_key = os.getenv("COHERE_API_KEY", "")

print(f"GROQ_API_KEY present   : {bool(api_key)}")
print(f"GROQ_API_KEY prefix    : {api_key[:12] + '...' if api_key else 'MISSING'}")
print(f"COHERE_API_KEY present : {bool(cohere_key)}")

if not api_key:
    print("CRITICAL: GROQ_API_KEY is missing. intelligence.py returns early → summary always fails.")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────
# PHASE 2 — PDF TEXT EXTRACTION
# ─────────────────────────────────────────────────────────────
section("PHASE 2: PDF Text Extraction Logic")

# Simulate the extract_text() function from upload_view.py
SAMPLE_TEXT = """
Machine learning is a field of artificial intelligence.
Supervised learning involves training a model on labeled data.
Neural networks are inspired by the structure of the human brain.
Deep learning uses multiple layers to learn complex representations.
Gradient descent is an optimization algorithm used to train models.
"""

print(f"Simulated text length  : {len(SAMPLE_TEXT)} chars")
print(f"Text is empty          : {not SAMPLE_TEXT.strip()}")

# Check what upload_view.py sends if extraction fails
failed_text = "PDF extraction failed."
print(f"\nWARNING CHECK: upload_view.py sends literal string '{failed_text}' on exception")
print(f"This means intelligence.py receives meaningless text and fails to generate a useful summary.")

# ─────────────────────────────────────────────────────────────
# PHASE 3 — INTELLIGENCE MODULE: _get_llm()
# ─────────────────────────────────────────────────────────────
section("PHASE 3: LLM Initialization (_get_llm)")

try:
    from langchain_groq import ChatGroq
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.3,
        api_key=api_key
    )
    print(f"ChatGroq init          : OK")
    print(f"Model                  : llama-3.3-70b-versatile")
except Exception as e:
    print(f"ChatGroq init FAILED   : {e}")
    traceback.print_exc()
    sys.exit(1)

# ─────────────────────────────────────────────────────────────
# PHASE 4 — INTELLIGENCE MODULE: prompt chain execution
# ─────────────────────────────────────────────────────────────
section("PHASE 4: LLM Prompt Chain Execution")

from langchain_core.prompts import ChatPromptTemplate

system_prompt = """You are a highly efficient AI assistant.
Your goal is to rapidly analyze the provided document excerpt and return a JSON object containing:
1. "summary": A concise, 2-3 sentence overview of the document's purpose.
2. "topics": A list of 3-5 core concepts or topics mentioned in the text.

Do NOT output anything other than valid JSON.
Format exactly like this:
{
  "summary": "...",
  "topics": ["...", "..."]
}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{text}")
])

chain = prompt | llm
sample_text = SAMPLE_TEXT[:4000]

print(f"Input text length      : {len(sample_text)} chars")
print(f"Input text empty       : {not sample_text.strip()}")

try:
    response = chain.invoke({"text": sample_text})
    raw_content = response.content.strip()
    print(f"\nRaw LLM response:\n{raw_content[:500]}")

    # Clean markdown wrapping (same logic as intelligence.py)
    content = raw_content
    if content.startswith("```json"):
        content = content[7:-3]
    elif content.startswith("```"):
        content = content[3:-3]

    data = json.loads(content)
    print(f"\nParsed summary : {data.get('summary', 'MISSING')[:100]}")
    print(f"Parsed topics  : {data.get('topics', [])}")
    print("\nINTELLIGENCE CHAIN: SUCCESS")

except json.JSONDecodeError as e:
    print(f"\nJSON PARSE FAILED: {e}")
    print(f"Raw content was: {raw_content[:500]}")
    traceback.print_exc()

except Exception as e:
    print(f"\nLLM CHAIN INVOCATION FAILED:")
    traceback.print_exc()

# ─────────────────────────────────────────────────────────────
# PHASE 5 — config.py `import config` side-effect check
# ─────────────────────────────────────────────────────────────
section("PHASE 5: config.py Import Side-effect")

print("Checking if 'import config' inside _get_llm() crashes when streamlit is absent...")
try:
    # intelligence.py does `import config` to get LLM_MODEL, LLM_TEMP
    # config.py does `import streamlit as st` at module level → this WILL fail outside Streamlit
    import config  # noqa
    llm_model = getattr(config, "LLM_MODEL", "llama-3.3-70b-versatile")
    llm_temp  = getattr(config, "LLM_TEMP", 0.3)
    print(f"config.LLM_MODEL       : {llm_model}")
    print(f"config.LLM_TEMP        : {llm_temp}")
    print("config import          : OK")
except Exception as e:
    print(f"config import FAILED   : {e}")
    print("NOTE: config.py imports streamlit at the top level.")
    print("      Inside Streamlit runtime, this is fine.")
    print("      But _get_llm() has a bare `import config` that may fail if")
    print("      config doesn't define LLM_MODEL / LLM_TEMP — those variables DO NOT exist in config.py!")
    traceback.print_exc()

section("PHASE 5b: config.py variable check")
print("Checking if config.py defines LLM_MODEL, LLM_TEMP, SELECTED_TOOL, TOOL_CONFIG...")
# Read raw file to check
config_path = os.path.join(SRC_DIR, "config.py")
with open(config_path, "r", encoding="utf-8-sig") as f:
    config_src = f.read()

for var in ["LLM_MODEL", "LLM_TEMP", "SELECTED_TOOL", "TOOL_CONFIG", "TOP_N_RERANK", "RETRIEVAL_K"]:
    found = var in config_src
    print(f"  {var:20s}: {'DEFINED' if found else '*** MISSING ***'}")

# ─────────────────────────────────────────────────────────────
# PHASE 6 — upload_view.py: text extraction race condition
# ─────────────────────────────────────────────────────────────
section("PHASE 6: upload_view.py extract_text() Issue")

print("upload_view.py reads the file with uploaded_file.read()")
print("Then intelligence calls extract_document_intelligence(text_content)")
print("BUT: if PDF is scanned/image-based, pypdf returns empty strings per page")
print("Joining empty strings gives empty text → LLM gets empty input → fails")
print()
print("Also: the bare 'except:' in extract_text() swallows ALL exceptions silently")
print("A corrupt PDF returns 'PDF extraction failed.' as the text content")
print("intelligence.py then sends THIS string to the LLM — it will return garbage or error")

# ─────────────────────────────────────────────────────────────
# PHASE 7 — workspace_view.py chat: missing vector store
# ─────────────────────────────────────────────────────────────
section("PHASE 7: Contextual Chat — No RAG / Vector Store")

print("workspace_view.py render_chat() uses doc['text'][:8000] as raw context")
print("This is a SIMPLE string truncation — NOT a RAG pipeline!")
print("The full FAISS/embeddings pipeline in backend/rag_engine.py is NEVER called from the UI.")
print("For large PDFs, only the first 8000 characters are used as context.")
print("This explains why chat answers may be incorrect or incomplete.")

# ─────────────────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────────────────
section("DIAGNOSIS SUMMARY")

issues = [
    ("CRITICAL", "intelligence.py line 73: bare `except Exception as e` swallows the full traceback — only prints e"),
    ("CRITICAL", "config.py has NO LLM_MODEL, LLM_TEMP, SELECTED_TOOL, TOOL_CONFIG variables — rag_engine.py will crash with AttributeError when these are accessed with getattr(config, ...) — BUT intelligence._get_llm() uses getattr with defaults so it silently gets wrong config"),
    ("CRITICAL", "upload_view.py extract_text(): bare `except:` silently returns 'PDF extraction failed.' string — LLM gets garbage input"),
    ("HIGH",     "If PDF is scanned/image-only, pypdf returns empty text — intelligence receives empty string, LLM returns error"),  
    ("HIGH",     "workspace_view.py contextual chat uses raw doc['text'][:8000] — full RAG pipeline never invoked"),
    ("HIGH",     "Status shows 'AI Ready' BEFORE intelligence.py has been called — no actual success validation"),
    ("MEDIUM",   "JSON parsing: if LLM returns text with markdown fencing like '```json\\n{...}\\n```', the slice [7:-3] may leave whitespace causing json.loads to fail"),
    ("MEDIUM",   "No retry mechanism on rate-limit errors from Groq API"),
]

for severity, desc in issues:
    print(f"[{severity}] {desc}")

print(f"\nDiagnostic complete.")
