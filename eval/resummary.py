"""Rebuild summary.md for an existing run from its results.jsonl."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EVAL_DIR = REPO_ROOT / "eval"
sys.path.insert(0, str(EVAL_DIR))

from run import write_summary  # noqa: E402


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: python eval/resummary.py <run_id>")
    run_dir = EVAL_DIR / "runs" / sys.argv[1]
    rows = [json.loads(l) for l in (run_dir / "results.jsonl").read_text().splitlines() if l.strip()]
    agents = sorted({r["agent"] for r in rows})
    models = sorted({r["model"] for r in rows})
    write_summary(run_dir, rows, agents, models)
    print(f"Wrote {run_dir / 'summary.md'}")


if __name__ == "__main__":
    main()
