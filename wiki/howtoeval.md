---
title: How to Evaluate AI Agents (Hylak)
type: summary
sources: [raw/howtoeval.md, https://www.howtoeval.com/]
updated: 2026-05-30
---

# How to Evaluate AI Agents

Practical guide by Ben Hylak, published May 2026. Opinionated,
anti-vendor-tooling: evaluating agents "is not that complicated."

## Audience

Teams shipping autonomous agents that replace human workflows (banking,
support, medical) — not expert-augmentation tools.

## Core framing

- **Benchmark maxxing** — chase public-leaderboard scores. (See [[vals-ai]].)
- **Floor raising** — fix real reliability failures where it matters.

## Pre-ship practices

- 5–10 golden cases.
- Inspect full agent trajectories locally.
- Ask the agent itself why it failed.

## Offline evals

Favor code-native harnesses (Vitest, pytest) over hosted dashboards. Cited
examples: Sentry's vitest-evals, OpenAI's "macro evals."

## Production loop

Stumbles → Issues → Signals → Experiments, scaled by volume.

## Iteration discipline

- Reproduce bugs before fixing.
- Prune low-signal eval cases.
- Spend ~10–20% of dev time on evaluation.

## Forward-looking thesis

As agents and models merge, "the harness collapses into the model itself."

## Author / vendor context

Hylak founded **Raindrop** (production agent monitoring) and **Raindrop
Workshop** (open-source local testing). Guide promotes both. Further reading
links Hamel Husain, Anthropic, OpenAI.

## Related

- Concept: [[llm-evaluation]]
- Contrast: [[vals-ai]] (third-party leaderboards) vs. in-house golden cases.
