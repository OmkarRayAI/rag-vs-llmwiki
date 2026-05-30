---
title: activegraph
type: summary
audience: internal
sources: [raw/activegraph.md, https://github.com/yoheinakajima/activegraph, https://pypi.org/project/activegraph/]
updated: 2026-05-30
---

# activegraph

Event-sourced reactive graph runtime for agentic systems. Authored by
Yohei Nakajima (BabyAGI). First release 2026-05-16, currently alpha.
Apache-2.0, Python >=3.11.

Tagline: "The graph is the world. Behaviors are physics. The trace is
the proof."

## Mental model

- **State** = typed graph of objects (e.g. `company`, `question`,
  `claim`, `evidence`, `risk`, `memo`) and relations (`addresses`,
  `derived_from`, `supports`).
- **Behaviors** = reactive functions pattern-matched against event
  shapes. No explicit workflow.
- **Trace** = append-only event log on disk. Runs are deterministic
  with fixtures and are resumable, forkable, and diff-able.

## CLI surface

`inspect`, `replay`, `fork`, `diff`, `export-trace`, `migrate`, `pack`,
`quickstart` (with `--interactive`).

## Diligence pack

Bundled IC-memo writer. Pipeline:

planner → question generator → document researcher → contradiction
finder → risk identifier → evidence linker → memo synthesizer.

Each memo cites evidence, lists risks, and explicitly states
contradictions or "none found." Pack-level invariant.

## Local quickstart, 2026-05-30

Ran offline in `/tmp/activegraph-sandbox` against bundled fixtures:
3 companies, 671 events, 103 LLM requests, ~25s wall clock, no network,
no API key. Output: structured memo per company with cited claims,
risks, and contradictions, persisted to SQLite.

## Relevance to this repo

Sits next to the [[llm-wiki-pattern]] as an alternative substrate for
LLM-maintained, citation-disciplined synthesis. See
[[agent-runtimes]] for the side-by-side and the v1 decision.

## Open threads

- Whether activegraph's event log + diff replaces git history over the
  markdown wiki, or complements it.
- Whether the Diligence pack's `claim`/`evidence`/`relation` graph could
  be exported back into a browsable markdown wiki.
- Stability: alpha, single author, two weeks old at ingest time.
