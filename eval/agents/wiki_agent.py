"""Wiki agent: answers from the curated wiki/ + AGENTS.md.

The whole wiki is small (~30KB). We stuff it into the system prompt and
ask the model to answer with citations.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _models import answer  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

SYSTEM = """You are a research librarian answering questions from a curated
markdown wiki. The wiki has been pre-synthesized: cross-period tables and
cross-source claims are already compiled into wiki/*.md pages.

Your job:
1. Read the wiki pages provided below.
2. Answer the user's question precisely.
3. Cite which wiki page each claim came from, e.g. [wiki/banking-sector-roundup.md].
4. If the wiki doesn't contain enough information to answer, say so explicitly.
5. Do NOT fabricate numbers. If a number isn't in the wiki, say "not in the wiki".

WIKI CONTENTS BELOW.
==================
"""


def load_wiki() -> str:
    parts = []
    for path in sorted((REPO_ROOT / "wiki").glob("*.md")):
        parts.append(f"\n\n=== {path.relative_to(REPO_ROOT)} ===\n")
        parts.append(path.read_text())
    parts.append(f"\n\n=== AGENTS.md ===\n")
    parts.append((REPO_ROOT / "AGENTS.md").read_text())
    return "".join(parts)


def query(question: str, model_id: str) -> str:
    system = SYSTEM + load_wiki()
    return answer(model_id, system, question)


if __name__ == "__main__":
    import sys
    q = sys.argv[1] if len(sys.argv) > 1 else "What was industry GNPA in 9M FY26?"
    model = sys.argv[2] if len(sys.argv) > 2 else "claude-sonnet-4-6"
    print(query(q, model))
