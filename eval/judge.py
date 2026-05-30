"""LLM-as-judge. Per fact in expected_facts, ask: did the answer assert it?"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _models import MODELS, answer  # noqa: E402

# Default to Gemini Flash: cheap, OpenRouter-accessible, strict on
# paraphrase. Override with EVAL_JUDGE_MODEL to use a different judge.
# Add the model id to MODELS in _models.py if it isn't already known.
JUDGE_MODEL = os.environ.get("EVAL_JUDGE_MODEL", "gemini-2.5-flash")
MODELS.setdefault("gemini-2.5-flash", "google/gemini-2.5-flash")

PROMPT = """You are grading whether an answer asserts a specific fact.

Question: {question}

Answer to grade:
\"\"\"
{ans}
\"\"\"

Fact: \"{fact}\"

Did the answer assert (or clearly imply) this fact? Numbers must match exactly
(within rounding). Reply with ONLY one word: YES or NO."""


def grade_fact(question: str, ans: str, fact: str) -> bool:
    user = PROMPT.format(question=question, ans=ans, fact=fact)
    resp = answer(JUDGE_MODEL, "You are a strict grader.", user).strip().upper()
    return resp.startswith("YES")


def grade(question: str, ans: str, expected_facts: list[str]) -> dict:
    results = []
    for fact in expected_facts:
        results.append({"fact": fact, "asserted": grade_fact(question, ans, fact)})
    correct = sum(r["asserted"] for r in results)
    return {
        "score": correct / len(results) if results else 0.0,
        "correct": correct,
        "total": len(results),
        "details": results,
    }
