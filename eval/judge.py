"""LLM-as-judge. Per fact in expected_facts, ask: did the answer assert it?"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _models import answer  # noqa: E402

JUDGE_MODEL = "claude-sonnet-4-6"

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
