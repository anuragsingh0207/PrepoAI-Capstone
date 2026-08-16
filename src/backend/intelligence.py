"""
intelligence.py — Production-grade document intelligence extraction.

ROOT CAUSE FIX:
  The original system_prompt used single curly braces { } in the JSON example block.
  LangChain's ChatPromptTemplate treats { } as template variable placeholders.
  This caused a KeyError on every invocation, which was silently caught by the
  bare `except Exception as e` block, returning "Could not generate summary at this time."

FIXES APPLIED:
  1. Escaped all literal { } in system_prompt as {{ }} so LangChain ignores them.
  2. Added empty text guard — returns early if extracted text is blank/whitespace.
  3. Improved JSON markdown stripping — handles leading/trailing whitespace robustly.
  4. Added full traceback logging so future failures are never silently swallowed.
  5. Added retry mechanism (up to 2 retries) for transient API/rate-limit errors.
  6. Exposed error detail in the returned dict for frontend debugging.
"""
import os
import json
import time
import traceback
import logging

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# ── Logging setup ──────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [intelligence] %(levelname)s: %(message)s"
)
logger = logging.getLogger("intelligence")


def _get_llm():
    """
    Initialise and return a ChatGroq LLM instance.
    Returns None if GROQ_API_KEY is not set.
    """
    try:
        import config
        llm_model = getattr(config, "GROQ_MODEL", getattr(config, "LLM_MODEL", "llama-3.3-70b-versatile"))
        llm_temp  = getattr(config, "LLM_TEMP",  0.3)
    except ImportError:
        llm_model = "llama-3.3-70b-versatile"
        llm_temp  = 0.3

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        logger.error("GROQ_API_KEY is not set. LLM cannot be initialised.")
        return None

    logger.info(f"Initialising ChatGroq: model={llm_model}, temp={llm_temp}")
    return ChatGroq(
        model=llm_model,
        temperature=llm_temp,
        api_key=api_key
    )


# ── System prompt ──────────────────────────────────────────────────────────────
# CRITICAL: All literal {{ }} braces are DOUBLED so LangChain does NOT treat
# them as template variables. This was the primary root cause of the failure.
_SYSTEM_PROMPT = """\
You are a highly efficient AI assistant.
Your goal is to rapidly analyze the provided document excerpt and return a JSON object containing:
1. "summary": A concise, 2-3 sentence overview of the document's purpose.
2. "topics": A list of 3-5 core concepts or topics mentioned in the text.

Do NOT output anything other than valid JSON.
Format EXACTLY like this (no markdown fencing, no extra text):
{{
  "summary": "...",
  "topics": ["...", "..."]
}}
"""


def _clean_json_response(raw: str) -> str:
    """
    Strip markdown code fences and surrounding whitespace from the LLM response.
    Handles: ```json ... ```, ``` ... ```, and plain JSON.
    """
    text = raw.strip()
    if text.startswith("```"):
        # Remove opening fence (```json or ```)
        first_newline = text.find("\n")
        if first_newline != -1:
            text = text[first_newline:].strip()
        # Remove closing fence
        if text.endswith("```"):
            text = text[:-3].strip()
    return text


def extract_document_intelligence(text_content: str, max_retries: int = 2) -> dict:
    """
    Extract a summary and key topics from document text using an LLM.

    Args:
        text_content: Raw extracted text from the uploaded document.
        max_retries:  Number of retry attempts on transient API errors.

    Returns:
        dict with keys:
            "summary" (str)  – 2-3 sentence overview
            "topics"  (list) – 3-5 key topics
            "error"   (str)  – populated only on failure, for frontend debugging
    """
    # ── Guard: empty input ────────────────────────────────────────────────────
    if not text_content or not text_content.strip():
        logger.warning("extract_document_intelligence received empty text. Skipping LLM call.")
        return {
            "summary": "No text could be extracted from this document. It may be a scanned image-based PDF.",
            "topics":  ["No extractable text"],
            "error":   "empty_input"
        }

    # ── Guard: extraction-failure sentinel ────────────────────────────────────
    failure_sentinels = {"PDF extraction failed.", "DOCX extraction failed."}
    if text_content.strip() in failure_sentinels:
        logger.warning(f"Text extraction failed upstream: '{text_content.strip()}'")
        return {
            "summary": "The document could not be read. Please try re-uploading a valid, text-based PDF.",
            "topics":  ["Document unreadable"],
            "error":   "upstream_extraction_failure"
        }

    # ── LLM init ──────────────────────────────────────────────────────────────
    llm = _get_llm()
    if not llm:
        return {
            "summary": "AI Summary is disabled — GROQ_API_KEY is missing.",
            "topics":  ["Setup required"],
            "error":   "missing_api_key"
        }

    # Truncate to first 4000 chars for speed and token budget
    sample_text = text_content[:4000]
    logger.info(f"Running intelligence extraction on {len(sample_text)} chars of text.")

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", _SYSTEM_PROMPT),
        ("human",  "{text}")
    ])
    chain = prompt_template | llm

    # ── Retry loop ────────────────────────────────────────────────────────────
    last_error = None
    for attempt in range(1, max_retries + 2):          # attempts: 1, 2, 3
        try:
            logger.info(f"LLM invoke attempt {attempt}/{max_retries + 1}")
            response     = chain.invoke({"text": sample_text})
            raw_content  = response.content
            clean_content = _clean_json_response(raw_content)

            logger.debug(f"Raw LLM response  : {raw_content[:200]}")
            logger.debug(f"Cleaned for parse : {clean_content[:200]}")

            data = json.loads(clean_content)

            summary = data.get("summary", "").strip()
            topics  = data.get("topics",  [])

            if not summary:
                raise ValueError("LLM returned empty summary field.")
            if not isinstance(topics, list):
                topics = [str(topics)]

            logger.info("Intelligence extraction succeeded.")
            return {"summary": summary, "topics": topics, "error": None}

        except json.JSONDecodeError as e:
            last_error = e
            logger.error(f"Attempt {attempt}: JSON parse failed. Raw response:\n{raw_content}\nError: {e}")
            # Don't retry JSON errors — the model likely misformatted; try again anyway once
            if attempt > 1:
                break

        except Exception as e:
            last_error = e
            full_tb = traceback.format_exc()
            logger.error(f"Attempt {attempt}: LLM call failed.\n{full_tb}")
            if attempt <= max_retries:
                wait = 2 ** attempt          # exponential back-off: 2s, 4s
                logger.info(f"Retrying in {wait}s...")
                time.sleep(wait)
            else:
                break

    # ── All attempts exhausted ────────────────────────────────────────────────
    error_str = str(last_error)
    logger.error(f"All {max_retries + 1} attempts failed. Last error: {error_str}")
    return {
        "summary": "Could not generate summary — the AI service returned an error. Check logs for details.",
        "topics":  ["Service Error"],
        "error":   error_str
    }
