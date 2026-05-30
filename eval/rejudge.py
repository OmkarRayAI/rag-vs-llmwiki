"""Re-grade rows whose previous judge call failed.

Reuses already-saved answers in eval/runs/<run_id>/results.jsonl. Skips rows
that graded cleanly. Uses a configurable judge model (default: cheap).

Usage:
    python eval/rejudge.py 20260530-033125
    python eval/rejudge.py 20260530-033125 --judge gemini-2.5-flash
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EVAL_DIR = REPO_ROOT / "eval"
sys.path.insert(0, str(EVAL_DIR))

from _models import MODELS, answer  # noqa: E402

# Add cheap judge models to the registry without disturbing answer-side ids.
MODELS.setdefault("gemini-2.5-flash", "google/gemini-2.5-flash")
MODELS.setdefault("haiku-4-5", "anthropic/claude-haiku-4.5")

PROMPT = """You are grading whether an answer asserts a specific fact.

Question: {question}

Answer to grade:
\"\"\"
{ans}
\"\"\"

Fact: \"{fact}\"

Did the answer assert (or clearly imply) this fact? Numbers must match exactly
(within rounding). Reply with ONLY one word: YES or NO."""


def grade_fact(question: str, ans: str, fact: str, judge_model: str) -> bool:
    user = PROMPT.format(question=question, ans=ans, fact=fact)
    resp = answer(judge_model, "You are a strict grader.", user).strip().upper()
    return resp.startswith("YES")


def needs_regrade(row: dict) -> bool:
    if row.get("answer", "").startswith("ERROR:"):
        return False
    return any(d.get("fact") == "JUDGE_ERROR" or "error" in d for d in row.get("details", []))


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())


def load_questions() -> dict:
    return {
        json.loads(l)["id"]: json.loads(l)
        for l in (EVAL_DIR / "golden" / "questions.jsonl").read_text().splitlines()
        if l.strip()
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("run_id")
    ap.add_argument("--judge", default="gemini-2.5-flash")
    args = ap.parse_args()

    load_env(REPO_ROOT / ".env")
    run_dir = EVAL_DIR / "runs" / args.run_id
    results_path = run_dir / "results.jsonl"
    if not results_path.exists():
        sys.exit(f"No results file: {results_path}")
    if args.judge not in MODELS:
        sys.exit(f"Unknown judge: {args.judge}. Known: {list(MODELS)}")

    rows = [json.loads(l) for l in results_path.read_text().splitlines() if l.strip()]
    qs = load_questions()

    targets = [r for r in rows if needs_regrade(r)]
    print(f"Regrading {len(targets)} of {len(rows)} rows with {args.judge}",
          file=sys.stderr)

    rejudged = 0
    for r in rows:
        if not needs_regrade(r):
            continue
        q = qs[r["qid"]]
        details = []
        for fact in q["expected_facts"]:
            try:
                ok = grade_fact(r["question"], r["answer"], fact, args.judge)
                details.append({"fact": fact, "asserted": ok})
            except Exception as e:
                details.append({"fact": fact, "asserted": False, "error": str(e)})
        correct = sum(d["asserted"] for d in details)
        r["details"] = details
        r["correct"] = correct
        r["total"] = len(details)
        r["score"] = correct / len(details) if details else 0.0
        r["regraded_with"] = args.judge
        rejudged += 1
        print(f"  {r['qid']} | {r['agent']} | {r['model']} -> {correct}/{len(details)}",
              file=sys.stderr)

    backup = results_path.with_suffix(".jsonl.pre-rejudge")
    if not backup.exists():
        backup.write_text(results_path.read_text())
    results_path.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    print(f"\nRegraded {rejudged} rows. Backup at {backup}", file=sys.stderr)
    print(f"Now run: python -c 'from run import write_summary' or rerun summary",
          file=sys.stderr)


if __name__ == "__main__":
    main()
