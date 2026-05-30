# activegraph

Source: https://github.com/yoheinakajima/activegraph
PyPI: https://pypi.org/project/activegraph/

Active Graph is an event-sourced reactive graph runtime for long-running,
auditable, agentic systems. Authored by Yohei Nakajima (BabyAGI). First
release on 2026-05-16. Latest version 1.0.5.post2 uploaded 2026-05-20.
Apache-2.0. Alpha status. Requires Python >=3.11.

Its tagline: "The graph is the world. Behaviors are physics. The trace is
the proof."

Core model:
- The state of the world is a typed graph of objects and relations.
- Behaviors are reactive functions pattern-matched against event shapes
  (e.g. `object.created` of type `question`). They are not orchestrated
  workflows.
- Every LLM call, tool call, patch, and object creation is an event in an
  append-only log on disk (SQLite by default, Postgres optional).
- Runs are deterministic when served by recorded fixtures, and are
  resumable, forkable, and diff-able from the event log.

Capabilities exposed via the CLI:
- `inspect` — status snapshot for a run.
- `replay` — rebuild the graph from events without re-firing behaviors.
- `fork` — copy events up to a point and branch a new run.
- `diff` — structural diff between two runs in the same store.
- `export-trace` — dump an event log as text or JSONL.
- `migrate` — copy runs across stores.
- `pack` — scaffold and list installed behavior packs.
- `quickstart` — run the bundled Diligence demo offline; `--interactive`
  walks through writing a custom behavior.

Packs are Python packages that register object types, relations,
behaviors, tools, prompts, and policies. The bundled Diligence pack
implements an investment-committee memo writer: planner -> question
generator -> document researcher -> contradiction finder -> risk
identifier -> evidence linker -> memo synthesizer. Output: per-company
memo with cited claims, listed risks, and explicit contradictions or a
"none found" statement (the pack's "verifiable memo bar").

Optional install extras: `[llm]`, `[anthropic]`, `[openai]`, `[postgres]`,
`[prometheus]`, `[all]`.

Quickstart demo metrics, observed locally on 2026-05-30:
- 3 companies, 671 events, 103 LLM requests, ~25s wall clock, fully
  offline against `RecordedDiligenceProvider` fixtures.
- Per-claim citations via `claim --derived_from--> document` and
  `evidence --supports--> claim` relations.

Differences from the LLMWiki pattern:
- Storage: SQLite event log + typed graph, vs. human-readable markdown
  files. activegraph traces are inspectable through CLI tooling; the
  wiki is browsable in a file tree or Obsidian.
- Synthesis trigger: reactive behaviors firing on event shape, vs.
  explicit Ingest / Query / Lint operations called by an agent against
  a schema in `AGENTS.md`.
- Auditability primitive: append-only event log with fork/diff, vs.
  git history over the markdown wiki.
- Maturity: alpha, two weeks old at time of writing, vs. Karpathy gist
  pattern that is implementation-agnostic and predates this repo.
