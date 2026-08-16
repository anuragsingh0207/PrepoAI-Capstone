"""
Final end-to-end verification of all fixes.
"""
import os, sys, json, traceback

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
sys.path.insert(0, SRC_DIR)

from dotenv import load_dotenv
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

PASS = "[PASS]"
FAIL = "[FAIL]"

results = []

def check(label, passed, detail=""):
    tag = PASS if passed else FAIL
    msg = f"{tag} {label}"
    if detail:
        msg += f"\n       {detail}"
    print(msg)
    results.append((passed, label))

print("=" * 65)
print("PrepoAI Full Verification — Post-Fix")
print("=" * 65)

# ── TEST 1: API Key ────────────────────────────────────────────────────────────
api_key = os.getenv("GROQ_API_KEY", "")
check("GROQ_API_KEY is set", bool(api_key), api_key[:14] + "..." if api_key else "MISSING")

# ── TEST 2: intelligence.py imports cleanly ────────────────────────────────────
try:
    from backend.intelligence import extract_document_intelligence, _get_llm
    check("intelligence.py imports without error", True)
except Exception as e:
    check("intelligence.py imports without error", False, str(e))

# ── TEST 3: _get_llm() returns a valid LLM ────────────────────────────────────
try:
    llm = _get_llm()
    check("_get_llm() returns ChatGroq instance", llm is not None, type(llm).__name__)
except Exception as e:
    check("_get_llm() returns ChatGroq instance", False, str(e))

# ── TEST 4: extract_document_intelligence with real text ──────────────────────
sample = """
Retrieval-Augmented Generation (RAG) is a hybrid AI architecture that combines
a retrieval system with a generative model. The retrieval component fetches
relevant passages from a knowledge base, while the generative model produces
a coherent answer conditioned on those passages. RAG reduces hallucination
and improves factual accuracy. FAISS is a popular library for efficient
similarity search used in RAG pipelines. LangChain provides orchestration
primitives for building such pipelines in Python.
"""
try:
    result = extract_document_intelligence(sample)
    summary_ok = bool(result.get("summary")) and "Could not" not in result["summary"] and "error" not in result["summary"].lower()[:20]
    topics_ok  = isinstance(result.get("topics"), list) and len(result["topics"]) > 0 and result["topics"] != ["N/A"] and result["topics"] != ["Service Error"]
    error_field = result.get("error")

    check("extract_document_intelligence returns valid summary", summary_ok,
          result.get("summary", "")[:120])
    check("extract_document_intelligence returns valid topics", topics_ok,
          str(result.get("topics", [])))
    check("extract_document_intelligence error field is None on success", error_field is None,
          f"error={error_field}")
except Exception as e:
    check("extract_document_intelligence works end-to-end", False, traceback.format_exc())

# ── TEST 5: Empty text guard ───────────────────────────────────────────────────
try:
    r = extract_document_intelligence("")
    check("Empty text returns safe fallback (not crash)",
          "error" in r and r["error"] == "empty_input",
          f"summary='{r.get('summary','')[:60]}' error='{r.get('error')}'")
except Exception as e:
    check("Empty text guard", False, str(e))

# ── TEST 6: Extraction failure sentinel guard ──────────────────────────────────
try:
    r = extract_document_intelligence("PDF extraction failed.")
    check("Extraction sentinel returns safe fallback",
          r.get("error") == "upstream_extraction_failure",
          f"error='{r.get('error')}'")
except Exception as e:
    check("Extraction sentinel guard", False, str(e))

# ── TEST 7: upload_view.py extract_text returns (text, error) tuple ───────────
try:
    from ui.views.upload_view import extract_text
    import io

    class FakeFile:
        def __init__(self, data, name):
            self.name = name
            self._data = data
        def read(self):
            return self._data

    fake_txt = FakeFile(b"Hello world test content for PrepoAI.", "test.txt")
    text, err = extract_text(fake_txt)
    check("upload_view.extract_text returns (text, None) for valid txt",
          text == "Hello world test content for PrepoAI." and err is None,
          f"text='{text}' err={err}")

    fake_empty = FakeFile(b"", "empty.txt")
    text2, err2 = extract_text(fake_empty)
    check("upload_view.extract_text returns ('', error_str) for empty file",
          text2 == "" and err2 is not None,
          f"err='{err2}'")
except Exception as e:
    check("upload_view.extract_text signature check", False, traceback.format_exc())

# ── TEST 8: workspace_view imports cleanly ────────────────────────────────────
try:
    from ui.views import workspace_view
    check("workspace_view.py imports without error", True)
except Exception as e:
    check("workspace_view.py imports without error", False, str(e))

# ── SUMMARY ───────────────────────────────────────────────────────────────────
print()
print("=" * 65)
passed = sum(1 for ok, _ in results if ok)
total  = len(results)
print(f"Results: {passed}/{total} checks passed")
if passed == total:
    print("ALL CHECKS PASSED — pipeline is healthy.")
else:
    print("SOME CHECKS FAILED:")
    for ok, label in results:
        if not ok:
            print(f"  FAIL: {label}")
print("=" * 65)
