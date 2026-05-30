"""Generate PNG charts from a finished eval run.

    python scripts/make_charts.py eval/runs/20260530-033125

Outputs:
    docs/charts/score_by_difficulty.png
    docs/charts/failure_modes.png

Style: matplotlib defaults, no seaborn, no theme. Print-readable, repo-friendly.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt

REPO_ROOT = Path(__file__).resolve().parent.parent
CHART_DIR = REPO_ROOT / "docs" / "charts"


def judged(row: dict) -> bool:
    return not any(d.get("fact") == "JUDGE_ERROR" for d in row.get("details", []))


def load_run(run_dir: Path) -> tuple[list[dict], dict]:
    rows = [
        json.loads(l)
        for l in (run_dir / "results.jsonl").read_text().splitlines()
        if l.strip()
    ]
    qs = {
        json.loads(l)["id"]: json.loads(l)
        for l in (REPO_ROOT / "eval" / "golden" / "questions.jsonl").read_text().splitlines()
        if l.strip()
    }
    return rows, qs


def chart_score_by_difficulty(rows: list[dict], qs: dict, out: Path) -> None:
    judged_rows = [r for r in rows if judged(r)]
    cells = {}
    for agent in ("wiki", "rag"):
        for diff in ("lookup", "synthesis"):
            sub = [r for r in judged_rows
                   if r["agent"] == agent and qs[r["qid"]]["difficulty"] == diff]
            c = sum(r["correct"] for r in sub)
            t = sum(r["total"] for r in sub)
            cells[(agent, diff)] = (c, t, 100 * c / t if t else 0)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    diffs = ["lookup", "synthesis"]
    x = range(len(diffs))
    w = 0.35
    wiki_pcts = [cells[("wiki", d)][2] for d in diffs]
    rag_pcts = [cells[("rag", d)][2] for d in diffs]

    b1 = ax.bar([i - w / 2 for i in x], wiki_pcts, w, label="LLMWiki", color="#1f6feb")
    b2 = ax.bar([i + w / 2 for i in x], rag_pcts, w, label="Vanilla RAG", color="#bf4544")

    for bar, (a, d) in zip(list(b1) + list(b2),
                           [("wiki", "lookup"), ("wiki", "synthesis"),
                            ("rag", "lookup"), ("rag", "synthesis")]):
        c, t, pct = cells[(a, d)]
        ax.text(bar.get_x() + bar.get_width() / 2, pct + 1.5,
                f"{c}/{t}\n{pct:.0f}%", ha="center", va="bottom", fontsize=9)

    ax.set_xticks(list(x))
    ax.set_xticklabels([d.title() for d in diffs])
    ax.set_ylabel("Facts asserted (%)")
    ax.set_ylim(0, 105)
    ax.set_title("LLMWiki vs RAG: facts asserted, by question difficulty\n"
                 "(GPT-5 mini, cleanly-judged subset)")
    ax.legend(loc="upper right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle=":", alpha=0.4)
    fig.tight_layout()
    fig.savefig(out, dpi=160)
    plt.close(fig)
    print(f"Wrote {out}")


# F1-F8 cells, hand-coded in wiki/eval-failure-taxonomy.md.
FAILURE_CELLS = {
    "F1 retrieval-missed-target-period": (
        "RAG", ["q5", "q6", "q7", "q11", "q12", "q14", "q15",
                "q21", "q22", "q26", "q27", "q31", "q32", "q34", "q36", "q29"]),
    "F2 rag-hallucination": ("RAG", ["q33"]),
    "F3 rag-empty-refusal": ("RAG", ["q9", "q25", "q30", "q31", "q34", "q36"]),
    "F4 rag-reasoning-slip": ("RAG", ["q28"]),
    "F5 wiki: answer-stops-short": ("Wiki", ["q8", "q2", "q29", "q34"]),
    "F6 wiki: coverage-blind-spot": ("Wiki", ["q6", "q19"]),
    "F7 judge: paraphrase-miss": ("Judge", ["q19", "q29", "q12"]),
    "F8 wiki: data-gap": ("Wiki", ["q9"]),
}


def chart_failure_modes(out: Path) -> None:
    labels = list(FAILURE_CELLS.keys())
    counts = [len(FAILURE_CELLS[l][1]) for l in labels]
    owners = [FAILURE_CELLS[l][0] for l in labels]
    color_map = {"RAG": "#bf4544", "Wiki": "#1f6feb", "Judge": "#9a8f00"}
    colors = [color_map[o] for o in owners]

    fig, ax = plt.subplots(figsize=(8, 5))
    ypos = list(range(len(labels)))
    bars = ax.barh(ypos, counts, color=colors)
    ax.set_yticks(ypos)
    ax.set_yticklabels(labels, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("Cells affected")
    ax.set_title("Where the failures live (n=31 imperfect cleanly-judged cells)\n"
                 "Hand-coded per Shankar (2026)")
    for bar, n in zip(bars, counts):
        ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
                str(n), va="center", fontsize=9)

    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in color_map.values()]
    ax.legend(handles, color_map.keys(), loc="lower right", title="Owner")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", linestyle=":", alpha=0.4)
    fig.tight_layout()
    fig.savefig(out, dpi=160)
    plt.close(fig)
    print(f"Wrote {out}")


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: scripts/make_charts.py <eval/runs/RUN_ID>")
    run_dir = Path(sys.argv[1])
    if not run_dir.is_absolute():
        run_dir = REPO_ROOT / run_dir
    rows, qs = load_run(run_dir)
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    chart_score_by_difficulty(rows, qs, CHART_DIR / "score_by_difficulty.png")
    chart_failure_modes(CHART_DIR / "failure_modes.png")


if __name__ == "__main__":
    main()
