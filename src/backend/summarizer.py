"""
summarizer.py — Production-grade multi-level document summarization engine.

Architecture:
  Each summary level is a completely independent pipeline with:
  - Its own retrieval strategy (chunk count, coverage, overlap priority)
  - Its own LLM parameters (temperature, max_tokens)
  - Its own highly engineered system prompt
  - Its own output structure specification
  - Its own token budget
  - Its own cognitive depth target

Levels:
  "quick"    → Executive flash overview. Speed-optimised. Student-friendly.
  "standard" → Structured IIT-professor-quality educational summary.
  "deep"     → Full academic analysis. Researcher + mentor level depth.

Usage:
    from backend.summarizer import run_summary_pipeline

    result = run_summary_pipeline(
        level="standard",          # "quick" | "standard" | "deep"
        text=doc["text"],
        vector_store=doc.get("vector_store"),  # optional FAISS store
        doc_name="myfile.pdf"
    )
    # result: {"content": str, "level": str, "char_count": int, "error": str|None}
"""

import os
import time
import traceback
import logging
from typing import Optional

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

logger = logging.getLogger("summarizer")


# ══════════════════════════════════════════════════════════════════════════════
#  LEVEL CONFIGURATION TABLE
#  Each entry drives retrieval, LLM params, and the prompt router.
# ══════════════════════════════════════════════════════════════════════════════

_LEVEL_CONFIG = {
    "quick": {
        "label":          "Quick Overview",
        "temperature":    0.2,          # Low — factual, no creative drift
        "max_tokens":     512,           # ~350-400 words max — brevity enforced
        "text_chars":     3500,          # Take only first 3500 chars (intro/abstract heavy)
        "rag_chunks":     3,             # 3 most relevant chunks if vector store available
        "rag_query":      "main topic summary key ideas overview introduction",
        "retry_max":      2,
    },
    "standard": {
        "label":          "Standard Summary",
        "temperature":    0.3,           # Slight creativity for better explanations
        "max_tokens":     1536,          # ~1000-1200 words — medium depth
        "text_chars":     8000,          # More context for concept coverage
        "rag_chunks":     6,             # 6 chunks — broader coverage
        "rag_query":      "key concepts definitions important sections explanations examples",
        "retry_max":      2,
    },
    "deep": {
        "label":          "In-Depth Analysis",
        "temperature":    0.4,           # More reasoning flexibility for analytical depth
        "max_tokens":     3072,          # ~2000-2500 words — comprehensive
        "text_chars":     12000,         # Full context window for maximum coverage
        "rag_chunks":     10,            # 10 chunks — exhaustive retrieval
        "rag_query":      "technical concepts architecture workflow methodology analysis applications limitations insights",
        "retry_max":      3,
    },
}


# ══════════════════════════════════════════════════════════════════════════════
#  SYSTEM PROMPTS — Three genuinely different cognitive architectures
# ══════════════════════════════════════════════════════════════════════════════

# ── QUICK OVERVIEW PROMPT ─────────────────────────────────────────────────────
# Cognitive target: Executive comprehension in 60 seconds.
# Structure: What + Why + Bullets. No technical depth.

_PROMPT_QUICK = """\
You are a concise academic advisor. Your job is to give a student a rapid, \
clear understanding of what a document is about in under 60 seconds of reading.

=== YOUR TASK ===
Read the document excerpt and produce a QUICK OVERVIEW.

=== STRICT OUTPUT STRUCTURE ===
Write EXACTLY in this format, no deviations:

## 📌 What Is This Document About?
[2-3 sentences. What is the document? What problem does it address? Who is it for?]

## 🎯 Key Ideas (At a Glance)
- [Idea 1 — one sentence, plain English]
- [Idea 2 — one sentence, plain English]
- [Idea 3 — one sentence, plain English]
- [Idea 4 if present — one sentence]
- [Idea 5 if present — one sentence]

## 💡 Why This Matters
[1-2 sentences. Real-world relevance or application of this document's content.]

## 🏷️ Topics Covered
[Comma-separated list of 4-6 key topics. Just the terms, no explanation.]

=== RULES — FOLLOW STRICTLY ===
1. Write for a first-year student who has never seen this topic.
2. NO technical jargon without immediate plain-English explanation.
3. NO filler phrases: "This document discusses...", "In conclusion...", "As we can see..."
4. DO NOT copy-paste sentences verbatim from the document.
5. Maximum reading time: 60 seconds. Be ruthlessly concise.
6. ONLY include information present in the provided text. Never hallucinate.
7. Start directly with ## 📌 — no preamble."""

# ── STANDARD SUMMARY PROMPT ──────────────────────────────────────────────────
# Cognitive target: Structured educational understanding.
# Like an IIT professor explaining to a 2nd-year student.
# Structure: Overview → Concepts → Relationships → Key Points → Revision Notes.

_PROMPT_STANDARD = """\
You are an expert IIT professor with 20 years of teaching experience in this subject.
A 2nd-year engineering student needs a thorough, well-structured study summary of this document.
Your output will be used as study notes — it must be educationally complete, not just descriptive.

=== YOUR TASK ===
Produce a STANDARD EDUCATIONAL SUMMARY that a student can use to understand and revise the material.

=== STRICT OUTPUT STRUCTURE ===

## 📖 Document Overview
[3-4 sentences: What this document covers, its purpose, and educational context. \
Mention the domain/subject area explicitly.]

## 🧠 Core Concepts Explained

For each major concept found in the document, write:
### [Concept Name]
**Definition:** [Clear, precise definition in 1-2 sentences]
**How it works:** [Explanation of the mechanism, process, or idea — 2-4 sentences]
**Why it matters:** [Relevance and significance — 1-2 sentences]

[Include ALL significant concepts from the document. Minimum 4, maximum 8.]

## 🔗 How Concepts Connect
[3-5 sentences explaining the relationships, dependencies, or workflow between the \
key concepts. Show how they form a coherent system or framework.]

## ⚡ Key Points for Exams
- **[Term/Concept]:** [One-line definition or key fact]
- [Repeat for 6-10 most important points]

## 📝 Revision Notes
[5-7 bullet points of the most exam-critical facts, definitions, or formulas from the document. \
Phrase them as a student would write in a revision sheet.]

## 🏷️ Topics & Subtopics
**Main subject:** [Primary field/domain]
**Key topics:** [Comma-separated list of 6-8 topics from the document]

=== RULES — FOLLOW STRICTLY ===
1. Write like you are teaching, not just describing.
2. Every concept must have a definition AND an explanation — never just one.
3. Use **bold** for all technical terms on first mention.
4. The "How Concepts Connect" section must show RELATIONSHIPS, not just list topics again.
5. Key Points must be genuinely exam-oriented — definitions, formulas, distinctions.
6. Do NOT copy-paste from the document. Paraphrase and explain in your own words.
7. Do NOT hallucinate concepts not in the provided text.
8. Do NOT use filler phrases or generic academic language.
9. If the document contains formulas or algorithms, explain them step by step.
10. Start directly with ## 📖 — no preamble or greetings."""

# ── IN-DEPTH ANALYSIS PROMPT ─────────────────────────────────────────────────
# Cognitive target: PhD-level analytical comprehension.
# Like an elite researcher + technical mentor dissecting the material.
# Structure: Critical analysis, architecture, implications, applications,
#            limitations, learning strategy.

_PROMPT_DEEP = """\
You are an elite AI researcher, senior technical architect, and IIT/MIT-level academic mentor \
with deep expertise in the subject domain of the provided document.

A graduate student or professional needs a COMPREHENSIVE ACADEMIC ANALYSIS of this document. \
This is NOT a summary — it is a deep, critical, multi-dimensional intellectual breakdown.

=== YOUR TASK ===
Produce a rigorous IN-DEPTH ANALYSIS that reveals everything important in this document, \
including what is implicit, what connects to broader knowledge, and what the practical implications are.

=== STRICT OUTPUT STRUCTURE ===

## 🔬 Document Intelligence Report
**Document type:** [Research paper / Textbook chapter / Technical report / Lecture notes / etc.]
**Primary domain:** [Field of study]
**Complexity level:** [Beginner / Intermediate / Advanced / Expert]
**Core thesis/purpose:** [1-2 sentences: the central argument or goal of this document]

---

## 📐 Conceptual Architecture

Map ALL major concepts and their structural relationships:

### [Concept 1 — Most Foundational]
- **Technical definition:** [Precise, formal definition]
- **Mechanism:** [How it functions, step by step if applicable]
- **Mathematical/formal representation:** [If applicable — formula, pseudocode, or notation]
- **Intuitive model:** [An analogy or simplified mental model]
- **Role in the system:** [How this concept feeds into or enables other concepts]

[Repeat this block for EVERY significant concept. Include ALL concepts mentioned in the text.]

---

## 🔄 System / Workflow Analysis
[If the document describes a process, algorithm, pipeline, or methodology:]
Provide a numbered step-by-step breakdown of the complete workflow/architecture, \
explaining what happens at each stage, why each step is necessary, and what could go wrong.

If no workflow: analyze the logical structure of the document's argument or framework instead.

---

## 🔍 Deep Analytical Insights

### What the document explicitly states:
[5-8 bullet points of the most important explicit claims/facts]

### What the document implies (reading between the lines):
[3-5 bullet points of inferences, assumptions, or implicit knowledge required]

### Critical observations:
[3-5 bullet points: limitations, potential failure modes, open questions, or trade-offs \
mentioned or implied in the document]

---

## 🌐 Broader Context & Applications

### Real-world applications:
[4-6 bullet points: Where and how are these concepts applied in practice?]

### Connections to related concepts:
[3-5 connections to adjacent topics, predecessor concepts, or follow-on technologies — \
ONLY if supported by content in the document]

### Strengths of the approach/content:
[3-4 bullet points]

### Limitations or gaps:
[3-4 bullet points — only if evident from the document content]

---

## 🧭 Learning Strategy & Mastery Guide

### Prerequisites you need to understand this:
[List 3-5 prerequisite concepts a reader needs]

### Concepts to master first (in order):
1. [Most foundational concept]
2. [Next concept to understand]
3. [Continue ordering...]

### High-yield exam/interview questions from this material:
- [Question 1 — deep conceptual]
- [Question 2 — application-based]
- [Question 3 — analytical]
- [Question 4 — comparison or trade-off]
- [Question 5 — design or implementation]

---

## 📊 Structured Revision Sheet

| Concept | Definition | Key Property | Example/Use Case |
|---------|-----------|--------------|-----------------|
| [Term 1] | [Definition] | [Property] | [Example] |
| [Term 2] | [Definition] | [Property] | [Example] |
[Include all major terms from the document in this table]

---

## 🏆 Expert Takeaways
[5-7 bullet points that an expert would identify as the most intellectually significant \
insights from this document — not just facts, but the "so what" behind the facts]

=== RULES — FOLLOW STRICTLY ===
1. This is an ANALYSIS, not a summary. Explain, critique, connect — don't just describe.
2. Every concept block must have ALL sub-fields filled. Never skip mechanism or intuitive model.
3. The table must include every significant term from the document.
4. "Implied insights" must be genuine inferences, not just restatements.
5. "Critical observations" must include at least one limitation or trade-off.
6. Use **bold** for technical terms and `code formatting` for algorithms/formulas.
7. NEVER hallucinate concepts not present or reasonably inferable from the text.
8. If the document is short, go deeper — extract maximum analytical value.
9. The revision table is MANDATORY. Do not omit it.
10. Start directly with ## 🔬 — no preamble, no greetings, no meta-commentary."""


# ══════════════════════════════════════════════════════════════════════════════
#  RETRIEVAL STRATEGY — Per-level RAG context building
# ══════════════════════════════════════════════════════════════════════════════

def _build_context(
    text: str,
    vector_store,
    level: str,
    doc_name: str
) -> str:
    """
    Build the document context string for the LLM.

    Strategy per level:
      quick    → First N chars only (intro-heavy, fast)
      standard → First N chars + RAG chunks deduplicated
      deep     → Full text up to limit + RAG chunks deduplicated
                 RAG chunks prioritize coverage of different sections

    Returns a single string ready to be injected into the HumanMessage.
    """
    cfg     = _LEVEL_CONFIG[level]
    n_chars = cfg["text_chars"]
    n_chunks = cfg["rag_chunks"]
    rag_query = cfg["rag_query"]

    # ── Base: raw text slice ──────────────────────────────────────────────────
    base_text = text[:n_chars].strip()

    if level == "quick" or vector_store is None:
        # Quick: just the raw text slice — no retrieval overhead
        logger.info(f"[SUMMARIZER] Context: raw text only ({len(base_text)} chars)")
        return f"Document: {doc_name}\n\n{base_text}"

    # ── Standard / Deep: augment with RAG retrieval ──────────────────────────
    try:
        retriever = vector_store.as_retriever(search_kwargs={"k": n_chunks})
        chunks    = retriever.invoke(rag_query)

        # Deduplicate: remove chunks whose content is already in base_text
        novel_chunks = []
        seen_content = set()
        for doc in chunks:
            content = doc.page_content.strip()
            # Skip if this chunk is a substring of base_text (already covered)
            if content[:80] in base_text:
                continue
            # Skip near-duplicate chunks
            key = content[:60].lower()
            if key in seen_content:
                continue
            seen_content.add(key)
            novel_chunks.append(content)

        if novel_chunks:
            rag_section = "\n\n--- Additional context from document ---\n" + \
                          "\n\n".join(f"[Passage {i+1}]: {c}" for i, c in enumerate(novel_chunks))
            context = f"Document: {doc_name}\n\n{base_text}{rag_section}"
        else:
            context = f"Document: {doc_name}\n\n{base_text}"

        logger.info(
            f"[SUMMARIZER] Context: {len(base_text)} chars base + "
            f"{len(novel_chunks)} novel RAG chunks = {len(context)} total chars"
        )
        return context

    except Exception:
        logger.warning(f"[SUMMARIZER] RAG retrieval failed, falling back to raw text:\n{traceback.format_exc()}")
        return f"Document: {doc_name}\n\n{base_text}"


# ══════════════════════════════════════════════════════════════════════════════
#  LLM FACTORY — Per-level parameter tuning
# ══════════════════════════════════════════════════════════════════════════════

def _get_level_llm(level: str) -> Optional[ChatGroq]:
    """
    Return a ChatGroq instance tuned for the given summary level.
    Each level has different temperature and max_tokens.
    """
    cfg     = _LEVEL_CONFIG.get(level, _LEVEL_CONFIG["standard"])
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        logger.error("[SUMMARIZER] GROQ_API_KEY not set")
        return None

    try:
        import config
        model = getattr(config, "GROQ_MODEL", getattr(config, "LLM_MODEL", "llama-3.3-70b-versatile"))
    except ImportError:
        model = "llama-3.3-70b-versatile"

    logger.info(
        f"[SUMMARIZER] LLM init: level={level}, model={model}, "
        f"temp={cfg['temperature']}, max_tokens={cfg['max_tokens']}"
    )

    return ChatGroq(
        model=model,
        temperature=cfg["temperature"],
        max_tokens=cfg["max_tokens"],
        api_key=api_key
    )


# ══════════════════════════════════════════════════════════════════════════════
#  PROMPT ROUTER — The dynamic dispatch core
# ══════════════════════════════════════════════════════════════════════════════

_PROMPT_ROUTER = {
    "quick":    _PROMPT_QUICK,
    "standard": _PROMPT_STANDARD,
    "deep":     _PROMPT_DEEP,
}


def _route_prompt(level: str) -> str:
    """Return the system prompt for the given level. Fails loudly on unknown level."""
    prompt = _PROMPT_ROUTER.get(level)
    if prompt is None:
        raise ValueError(
            f"Unknown summary level: '{level}'. "
            f"Valid levels: {list(_PROMPT_ROUTER.keys())}"
        )
    logger.info(f"[SUMMARIZER] Routing to prompt: {level} ({len(prompt)} chars)")
    return prompt


# ══════════════════════════════════════════════════════════════════════════════
#  POST-PROCESSOR — Validate and repair LLM output
# ══════════════════════════════════════════════════════════════════════════════

def _validate_output(content: str, level: str) -> tuple[bool, list[str]]:
    """
    Check that the output has the expected structural markers for the given level.
    Returns (is_valid, list_of_missing_sections).
    """
    required = {
        "quick":    ["## 📌", "## 🎯", "## 💡", "## 🏷️"],
        "standard": ["## 📖", "## 🧠", "## 🔗", "## ⚡", "## 📝"],
        "deep":     ["## 🔬", "## 📐", "## 🔍", "## 🌐", "## 🏆"],
    }
    checks  = required.get(level, [])
    missing = [s for s in checks if s not in content]
    return len(missing) == 0, missing


def _repair_truncated_output(content: str) -> str:
    """
    If the output appears truncated (no ending punctuation / ends mid-sentence),
    append a graceful completion note rather than returning broken markdown.
    """
    stripped = content.rstrip()
    if stripped and stripped[-1] not in ".!?|─—\n":
        # Likely truncated — close it gracefully
        content = stripped + "\n\n---\n*[Note: Output truncated at token limit. " \
                             "Try generating again for a complete response.]*"
    return content


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN PIPELINE ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def run_summary_pipeline(
    level: str,
    text: str,
    vector_store=None,
    doc_name: str = "document"
) -> dict:
    """
    Execute the full multi-level summarization pipeline.

    Args:
        level:         "quick" | "standard" | "deep"
        text:          Full extracted document text
        vector_store:  Optional FAISS vector store for RAG augmentation
        doc_name:      Document filename for context attribution

    Returns:
        {
            "content":    str   — the formatted summary (markdown),
            "level":      str   — the level used,
            "label":      str   — human-readable level name,
            "char_count": int   — output length,
            "strategy":   str   — retrieval strategy used,
            "error":      str | None
        }
    """
    t_start = time.time()
    cfg     = _LEVEL_CONFIG.get(level)

    if cfg is None:
        return {
            "content":    "",
            "level":      level,
            "label":      "Unknown",
            "char_count": 0,
            "strategy":   "none",
            "error":      f"Invalid level: '{level}'"
        }

    logger.info(f"[SUMMARIZER] ═══ Starting pipeline: level={level}, doc='{doc_name}' ═══")

    # ── Guard: empty text ─────────────────────────────────────────────────────
    if not text or not text.strip():
        return {
            "content":    "",
            "level":      level,
            "label":      cfg["label"],
            "char_count": 0,
            "strategy":   "none",
            "error":      "empty_document"
        }

    # ── Step 1: Route prompt ──────────────────────────────────────────────────
    try:
        system_prompt = _route_prompt(level)
    except ValueError as e:
        return {"content": "", "level": level, "label": cfg["label"],
                "char_count": 0, "strategy": "none", "error": str(e)}

    # ── Step 2: Build context (retrieval strategy) ────────────────────────────
    strategy = "rag_augmented" if (vector_store and level != "quick") else "raw_text"
    context  = _build_context(text, vector_store, level, doc_name)
    logger.info(f"[SUMMARIZER] Context built: {len(context)} chars | strategy={strategy}")

    # ── Step 3: Get level-tuned LLM ───────────────────────────────────────────
    llm = _get_level_llm(level)
    if llm is None:
        return {
            "content":    "",
            "level":      level,
            "label":      cfg["label"],
            "char_count": 0,
            "strategy":   strategy,
            "error":      "missing_api_key"
        }

    # ── Step 4: Build messages ────────────────────────────────────────────────
    sys_msg  = SystemMessage(content=system_prompt)
    user_msg = HumanMessage(
        content=(
            f"Please generate a {cfg['label']} for the following document.\n\n"
            f"{context}"
        )
    )

    # ── Step 5: Invoke with retry ─────────────────────────────────────────────
    max_attempts = cfg["retry_max"]
    last_error   = None
    content      = ""

    for attempt in range(1, max_attempts + 1):
        try:
            logger.info(f"[SUMMARIZER] LLM invoke attempt {attempt}/{max_attempts}")
            resp    = llm.invoke([sys_msg, user_msg])
            content = resp.content.strip()

            if not content:
                raise ValueError("LLM returned empty response")

            logger.info(
                f"[SUMMARIZER] LLM responded: {len(content)} chars in "
                f"{time.time() - t_start:.1f}s"
            )
            break  # success

        except Exception as e:
            last_error = e
            logger.error(f"[SUMMARIZER] Attempt {attempt} failed: {e}\n{traceback.format_exc()}")
            if attempt < max_attempts:
                wait = 2 ** attempt
                logger.info(f"[SUMMARIZER] Retrying in {wait}s...")
                time.sleep(wait)

    if not content:
        return {
            "content":    "",
            "level":      level,
            "label":      cfg["label"],
            "char_count": 0,
            "strategy":   strategy,
            "error":      str(last_error)
        }

    # ── Step 6: Validate structure ────────────────────────────────────────────
    is_valid, missing = _validate_output(content, level)
    if not is_valid:
        logger.warning(
            f"[SUMMARIZER] Output missing sections: {missing}. "
            f"Serving anyway (content present)."
        )

    # ── Step 7: Repair truncation ─────────────────────────────────────────────
    content = _repair_truncated_output(content)

    elapsed = time.time() - t_start
    logger.info(
        f"[SUMMARIZER] ═══ Pipeline complete: level={level}, "
        f"{len(content)} chars, {elapsed:.1f}s ═══"
    )

    return {
        "content":    content,
        "level":      level,
        "label":      cfg["label"],
        "char_count": len(content),
        "strategy":   strategy,
        "error":      None
    }
