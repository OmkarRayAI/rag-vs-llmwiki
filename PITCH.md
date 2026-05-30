# LLMWiki for Corporate Finance

A self-maintaining wiki for corporate-finance research, paired with an eval
harness that benchmarks it head-to-head against a vanilla RAG baseline on
**Vals CorpFin v2 / Finance Agent v2**.

## The claim

> Wiki-grounded synthesis beats retrieval-only RAG on real corp-fin
> questions. Here is the number, here is the harness, here are the
> questions we still get wrong.

## Why this exists

Most "agent + docs" demos are RAG: chunk, embed, retrieve, generate. Each
query rediscovers the same facts. The Karpathy LLM-wiki pattern compiles
synthesis once, into a durable, interlinked markdown graph the agent reads
and edits. We test the difference, on a public benchmark, in the open.

## What's in the repo

```
raw/        # immutable source documents (10-Ks, sector roundups, IRS pubs, ...)
wiki/       # LLM-maintained pages: entities, concepts, summaries
eval/
  baseline-rag/   # vanilla RAG: chunk + embed + top-k + generate
  wiki-agent/     # ingest -> wiki -> answer-from-wiki agent
  corpfin-runner  # runs both against Vals CorpFin v2 / Finance Agent v2
  golden/         # 10 hand-curated internal cases (per howtoeval.com)
AGENTS.md   # wiki schema (the "config")
PITCH.md    # this file
```

## Headline metrics

50 hand-authored corp-fin questions, 173 expected facts, GPT-5 mini
answering both sides. Full dataset, fully judged (split judge: GPT-5
mini for q1–q18, Gemini 2.5 Flash for q19–q50 after the original
judge ran out of credits):

| Question type           | Wiki agent       | RAG baseline    |
|-------------------------|-----------------:|----------------:|
| Lookup (single-period)  | 39/54 (72%)      | 31/54 (57%)     |
| Synthesis (cross-period)| 106/119 (89%)    | 17/119 (14%)    |
| Aggregate               | 145/173 (84%)    | 48/173 (28%)    |

Run id: `eval/runs/20260530-033125/`. RAG: 350-word chunks of the 6
PDFs, sentence-transformers MiniLM-L6 embeddings, top-8 retrieval.
Wiki: full `wiki/*.md` (~24 KB) stuffed into the system prompt.

See `README.md` for charts and `wiki/eval-failure-taxonomy.md` for
the F1–F8 hand-coded breakdown of every wrong cell.

### Where the gap comes from

100% of RAG's failures are retrieval-driven (codes F1+F2+F3+F4 in the
taxonomy). Top-k over visually-heavy slide PDFs couldn't surface the
right page for cross-period questions. Sample RAG response (q5, *CASA
trend across 6 periods*):

> *"I cannot provide period-by-period industry CASA ratio numbers
> because the provided passages do not contain industry CASA ratio
> values for H1 FY25, FY26, or 9M FY26."*

The figures were in the PDF corpus. The retriever just didn't surface
them. The wiki had all six periods in a single pre-built table, so
the question was a lookup.

Total cost of this run: under $2 via OpenRouter.

## Failures we publish

Per-fact grading missed subtle hallucinations even on cells scored
"correct" (e.g., reading the highest figure of a range as a specific
period value). The judge also marked NO when answers asserted the
fact in different words (taxonomy code F7, ≥3 cells). The next
iteration of the eval — per [howtoeval.com](https://www.howtoeval.com/)
"floor raising" — should:

1. Tighten the judge before adding more questions.
2. Tighten the wiki agent prompt to volunteer secondary facts (F5).
3. Patch the FY25 NIM YoY gap in `wiki/banking-sector-roundup.md` (F8).
4. Re-grade the 14 `JUDGE_ERROR` cells once OpenRouter is topped up.

## Failures we publish

Per Hylak ([howtoeval.com](https://www.howtoeval.com/)), the signal is in
what breaks. We commit a fixed set of 10 internal golden cases and show,
per release, which ones each system gets wrong. No cherry-picking. The
failure log lives in `eval/golden/failures.md` and is part of the README.

## Roadmap

1. **Lock the corpus.** Freeze a versioned `raw/` snapshot. Reproducible
   numbers require a frozen input set.
2. **Build the baseline.** Vanilla RAG. Boring on purpose. This is the
   thing we have to beat.
3. **Compile the wiki.** Run ingest over `raw/`. The wiki's quality is the
   experiment.
4. **Wire the runner.** Drive both systems against Vals CorpFin v2 and
   Finance Agent v2. Identical model, identical prompts at the answer
   layer.
5. **Author 10 golden cases.** Real questions a corp-fin analyst would ask.
   These exist to catch what the public benchmark misses.
6. **Publish.** Numbers, failures, replication command. One README, one
   diagram, one GIF.
7. **(Stretch) TaxEval.** If the harness generalizes, a tax-corpus
   instance is a follow-up post, not a v1 feature.

## Non-goals

- Beating SOTA on every Vals leaderboard. We pick two benchmarks aligned
  with the corpus and run them honestly.
- A hosted product, a UI, a SaaS dashboard. The repo *is* the artifact.
- Embeddings everywhere. Embeddings appear in the baseline because the
  baseline is RAG. The wiki agent uses the link graph; we add embeddings
  only if we prove the graph is insufficient.
- A "framework." No plugin system, no abstractions for hypothetical second
  users. One vertical, one harness.

## What "done" looks like

A reader lands on the README, sees one table, one diagram, one GIF, and
one command:

```
git clone ... && make eval
```

…and reproduces the numbers on their own machine in under an hour.

## Source pointers

- Pattern origin: Karpathy LLM-wiki gist (`raw/karpathy-llm-wiki.md`).
- Eval philosophy: Hylak, *How to Evaluate AI Agents*
  (`raw/howtoeval.md`).
- Benchmark host: Vals AI (`raw/vals-ai.md`), specifically CorpFin v2 and
  Finance Agent v2.
- RAG baseline reference: Lewis et al., 2020 (`raw/rag.md`).
