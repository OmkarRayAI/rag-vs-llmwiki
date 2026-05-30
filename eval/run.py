"""Run the eval: questions x agents x models, score, write summary."""

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
sys.path.insert(0, str(REPO_ROOT))

from agents import rag_agent, wiki_agent  # noqa: E402
from judge import grade  # noqa: E402

# Opt-in tracing: set WIKITRACE=1 to record a trace alongside results.jsonl.
WIKITRACE = os.environ.get("WIKITRACE") == "1"
if WIKITRACE:
    import wikitrace  # noqa: E402

AGENTS = {"wiki": wiki_agent.query, "rag": rag_agent.query}
MODELS = ["claude-sonnet-4-6", "gpt-5-mini"]


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())


def load_questions() -> list[dict]:
    path = EVAL_DIR / "golden" / "questions.jsonl"
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", choices=list(AGENTS) + ["all"], default="all")
    ap.add_argument("--model", choices=MODELS + ["all"], default="all")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--resume", help="Run id (timestamp) to resume; skips cells already in results.jsonl")
    args = ap.parse_args()

    load_env(REPO_ROOT / ".env")
    questions = load_questions()
    if args.limit:
        questions = questions[: args.limit]

    agents = list(AGENTS) if args.agent == "all" else [args.agent]
    models = MODELS if args.model == "all" else [args.model]

    if args.resume:
        run_dir = EVAL_DIR / "runs" / args.resume
        if not run_dir.exists():
            sys.exit(f"No run dir: {run_dir}")
        run_id = args.resume
    else:
        run_id = time.strftime("%Y%m%d-%H%M%S")
        run_dir = EVAL_DIR / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    results_path = run_dir / "results.jsonl"

    done: set[tuple[str, str, str]] = set()
    rows: list[dict] = []
    if results_path.exists():
        for line in results_path.read_text().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            done.add((r["qid"], r["agent"], r["model"]))
            rows.append(r)
        print(f"Resuming run {run_id}: {len(done)} cells already done", file=sys.stderr)
    print(f"Run: {run_dir}", file=sys.stderr)

    if WIKITRACE:
        wikitrace.init(pipeline="eval",
                       trace_dir=str(REPO_ROOT / ".wikitrace"),
                       attrs={"run_id": run_id, "live": True})
        live_root = wikitrace.span("eval", run_id=run_id, live=True)
        live_root.__enter__()

    f = results_path.open("a")
    try:
        for q in questions:
            for agent_name in agents:
                for model_id in models:
                    key = (q["id"], agent_name, model_id)
                    if key in done:
                        continue
                    tag = f"{q['id']} | {agent_name} | {model_id}"
                    print(f"-> {tag}", file=sys.stderr)
                    t0 = time.time()
                    if WIKITRACE:
                        agent_span = wikitrace.span("agent_call",
                                                    qid=q["id"],
                                                    agent=agent_name,
                                                    model=model_id)
                        agent_span.__enter__()
                    try:
                        ans = AGENTS[agent_name](q["question"], model_id)
                    except Exception as e:
                        ans = f"ERROR: {e}"
                    latency = time.time() - t0
                    if WIKITRACE:
                        agent_span.__exit__(None, None, None)
                    if ans.startswith("ERROR:"):
                        score = {"score": 0.0, "correct": 0, "total": len(q["expected_facts"]), "details": []}
                    else:
                        try:
                            score = grade(q["question"], ans, q["expected_facts"])
                        except Exception as e:
                            score = {"score": 0.0, "correct": 0, "total": len(q["expected_facts"]),
                                     "details": [{"fact": "JUDGE_ERROR", "asserted": False, "error": str(e)}]}
                    row = {
                        "qid": q["id"], "agent": agent_name, "model": model_id,
                        "question": q["question"], "answer": ans,
                        "score": score["score"], "correct": score["correct"],
                        "total": score["total"], "details": score["details"],
                        "latency_s": round(latency, 2),
                    }
                    rows.append(row)
                    f.write(json.dumps(row) + "\n")
                    f.flush()
                    print(f"   score: {score['correct']}/{score['total']}  ({latency:.1f}s)", file=sys.stderr)
    finally:
        f.close()
        if WIKITRACE:
            live_root.__exit__(None, None, None)
            wikitrace.end()

    write_summary(run_dir, rows, agents, models)
    print(f"\nSummary: {run_dir / 'summary.md'}", file=sys.stderr)


def write_summary(run_dir: Path, rows: list[dict], agents: list[str], models: list[str]) -> None:
    lines = [f"# Eval run {run_dir.name}", ""]
    lines.append("## Aggregate score (correct facts / total facts)")
    lines.append("")
    lines.append("| Model | " + " | ".join(agents) + " |")
    lines.append("|" + "---|" * (len(agents) + 1))
    for m in models:
        cells = [m]
        for a in agents:
            sub = [r for r in rows if r["agent"] == a and r["model"] == m]
            c = sum(r["correct"] for r in sub)
            t = sum(r["total"] for r in sub)
            cells.append(f"{c}/{t} ({100 * c / t:.0f}%)" if t else "-")
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("## Per-question detail")
    for qid in sorted({r["qid"] for r in rows}):
        lines.append(f"\n### {qid}")
        sample = next(r for r in rows if r["qid"] == qid)
        lines.append(f"\n> {sample['question']}\n")
        lines.append("| Agent | Model | Score | Latency |")
        lines.append("|---|---|---|---|")
        for r in [x for x in rows if x["qid"] == qid]:
            lines.append(f"| {r['agent']} | {r['model']} | {r['correct']}/{r['total']} | {r['latency_s']}s |")
    (run_dir / "summary.md").write_text("\n".join(lines))


if __name__ == "__main__":
    main()
