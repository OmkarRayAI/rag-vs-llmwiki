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

First end-to-end run: 5 hand-authored corp-fin questions over the 6
BCG decks. Same questions, same models, same source PDFs. Only the
retrieval/synthesis strategy differs.

| System         | Sonnet 4.6     | GPT-5 mini     |
|----------------|---------------:|---------------:|
| Baseline RAG   |  9/23 (39%)    |  9/23 (39%)    |
| LLMWiki agent  | 23/23 (100%)   | 23/23 (100%)   |

Run id: `eval/runs/20260530-024220/`. RAG: 350-word chunks of the 6
PDFs, sentence-transformers MiniLM-L6 embeddings, top-8 retrieval.
Wiki: full `wiki/*.md` (~24 KB) stuffed into the system prompt.

### Where the gap comes from

RAG matched the wiki on the two questions answerable from a single
section of one deck (the 9M FY26 ROA-tree table; the rate-cycle
narrative). RAG scored 0 on all three cross-period synthesis questions
(MSME vs. retail across 6 periods; PAT deceleration FY25→FY26; CASA
trend across 6 periods). Failure mode: top-k pulled fragments from
individual decks but couldn't compose the longitudinal view. Sample
RAG response: *"I can only provide data through 9M FY25 — there is no
data available for 9M FY26 in the provided passages."* The relevant
9M FY26 chunks existed in the index; the retriever just didn't
surface them for that query.

The wiki had the cross-period tables pre-compiled in
`wiki/banking-sector-roundup.md` and `wiki/indian-banking-fy25-fy26.md`,
so those questions reduced to lookups.

Total cost of this run: under $1 via OpenRouter.

## Failures we publish

Even at 23/23 the wiki agent got numbers wrong inside otherwise-correct
answers (e.g., reading the highest figure of a range as the FY25
specific value). Per-fact grading missed these because the expected
fact was the range itself. This is the kind of subtle hallucination
the next iteration of the eval (and the in-house golden suite per
[howtoeval.com](https://www.howtoeval.com/)) needs to catch.

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
