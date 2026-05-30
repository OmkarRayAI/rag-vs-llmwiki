# Eval

Smallest end-to-end harness for `PITCH.md`'s headline claim:

> Wiki-grounded synthesis beats vanilla RAG on Indian-banking questions.

## Layout

```
eval/
  golden/
    questions.jsonl    # 5 hand-authored questions over the BCG corpus
  runs/                # output of each run, gitignored except for the
                       # latest `summary.md` checked in for the README
  agents/
    wiki_agent.py      # answers from wiki/ markdown files
    rag_agent.py       # answers via Voyage embeddings + top-k over BCG PDFs
  judge.py             # LLM-as-judge: scores answers against expected_facts
  run.py               # loops questions x agents x models, writes results
```

## Setup

Keys go in `.env` at repo root (gitignored). Required:

- `OPENROUTER_API_KEY` — unified API for Sonnet 4.6 + GPT-5 mini.
- `PULSE_API_KEY` — only needed if regenerating parsed PDFs.

Embeddings for the RAG baseline are local (sentence-transformers/
all-MiniLM-L6-v2), no API key.

Then:

```bash
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python -r eval/requirements.txt
.venv/bin/python eval/run.py
```

## Question file shape

```jsonl
{
  "id": "q1-msme-vs-retail",
  "question": "...",
  "expected_facts": ["MSME outpaced retail in every period", ...],
  "difficulty": "lookup" | "synthesis",
  "needs": "cross-period table" | ...
}
```

## Scoring

LLM-as-judge with a binary rubric per fact: did the answer assert this
fact? Score = facts_correct / facts_total. Per-question and aggregate
scores written to `eval/runs/<timestamp>/summary.md`.

## Cost guard

`run.py` prints a cost estimate and aborts if it exceeds `MAX_USD`
(default $1) unless `--yes` is passed. One full run on 5 questions /
2 agents / 2 models with cheap-tier models ≈ $0.40.
