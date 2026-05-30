---
title: LLM Evaluation
type: concept
audience: internal
sources: [raw/vals-ai.md, raw/howtoeval.md]
updated: 2026-05-30
---

# LLM Evaluation

Evaluation of large language models and LLM-powered agents. Two broad
strategies sit in tension:

## Benchmark maxxing

Optimize for public, third-party leaderboards. Useful for cross-model
comparison and procurement; weak signal for production reliability of a
specific deployed agent.

- Independent benchmark aggregator: [[vals-ai]].
- Domains covered there: coding, finance, healthcare, legal, math/academic,
  plus aggregate indices (Vals Index, Vals Multimodal Index).
- Common public benchmarks: SWE-bench Verified, Terminal-Bench, GPQA
  Diamond, MMLU Pro, MMMU, LegalBench.

## Floor raising

Fix the failures that actually break a production agent. Per [[howtoeval]]:

- 5–10 golden cases curated by hand.
- Inspect full trajectories locally.
- Ask the agent why it failed.
- Code-native harnesses (Vitest, pytest, Sentry vitest-evals, OpenAI macro
  evals) over hosted dashboards.
- Production feedback loop: Stumbles → Issues → Signals → Experiments.
- Reproduce before fixing; prune low-signal cases; budget ~10–20% of dev
  time on eval work.

## Vendors / tooling mentioned

- **Vals AI** — third-party benchmarking and leaderboards. See [[vals-ai]].
- **Raindrop** — production agent monitoring (Hylak).
- **Raindrop Workshop** — open-source local testing harness (Hylak).
- **Sentry vitest-evals**, **OpenAI macro evals** — code-native eval
  patterns cited in [[howtoeval]].

## Forward-looking

Hylak's thesis: as agents and underlying models merge, "the harness
collapses into the model itself" — separate eval scaffolding becomes less
distinct from model capability work.

## Open threads

- Where does RAG eval fit? (See [[rag]] in raw.)
- Methodology comparison: how Vals AI runs its benchmarks vs. what an
  in-house golden-case suite would catch.
