---
title: Agent Runtimes
type: concept
audience: internal
sources: [raw/karpathy-llm-wiki.md, raw/activegraph.md, raw/howtoeval.md]
updated: 2026-05-30
---

# Agent Runtimes

Substrates an LLM-driven agent uses to *persist synthesis* and *prove its
reasoning is grounded*. Two reference points so far in this wiki:

- [[llm-wiki-pattern]] — Karpathy's gist. Markdown files in a `wiki/`
  directory, schema in `AGENTS.md`, three operations: Ingest, Query,
  Lint. Provenance via `[[links]]` and frontmatter `sources:`. Audit
  trail via git.
- [[activegraph]] — Nakajima's runtime. Typed graph of objects and
  relations, reactive behaviors fired by event shape, append-only event
  log on SQLite/Postgres. Provenance via `claim --derived_from-->
  document` relations. Audit trail via the event log itself, plus
  `fork` and `diff` over runs.

## Side-by-side

| Dimension                | LLM-wiki pattern                              | activegraph                                        |
|--------------------------|------------------------------------------------|----------------------------------------------------|
| Storage                  | Markdown files in a directory                  | SQLite/Postgres event log + typed object graph     |
| Reader experience        | Browsable in a file tree or Obsidian           | Inspected via CLI (`inspect`, `replay`, `diff`)    |
| Synthesis trigger        | Explicit Ingest/Query/Lint called by an agent  | Reactive behaviors pattern-matched on events       |
| Citation primitive       | `[[wiki/page]]` links + `sources:` frontmatter | `claim --derived_from--> document` graph relations |
| Audit primitive          | git log over markdown                          | Append-only event log; runs forkable + diff-able   |
| Schema location          | `AGENTS.md` (prose conventions)                | Pack registration (object types, relations, etc.)  |
| Maturity                 | Pattern, implementation-agnostic               | Alpha runtime, single author, two weeks old        |
| Differentiator           | Human-readable artifact                        | Determinism, replay, fork-and-diff over runs       |

## Where they overlap

Both want **citation-disciplined synthesis** that is **inspectable
after the fact**. Both reject pure RAG (rediscover-on-each-query) in
favor of a durable artifact. Both treat the schema as load-bearing.

## Where they diverge

- The wiki pattern bets on **humans reading markdown**. activegraph bets
  on **tooling reading event logs**. If the user is the librarian, the
  wiki wins; if the user is auditing an autonomous run, activegraph
  wins.
- The wiki has no opinion on *when* synthesis happens (the user runs
  Ingest). activegraph's runtime *is* an opinion: behaviors fire when
  their patterns match.

## Decision for this repo (`PITCH.md`)

v1 stays on the wiki pattern. Reasons:
1. The headline benchmark in `PITCH.md` compares wiki-grounded
   synthesis against vanilla RAG. Adding activegraph as a third
   variable confounds the comparison.
2. activegraph is alpha; basing a "production-grade" claim on a
   two-week-old runtime would be hard to defend.
3. The wiki's differentiator — human-browsable markdown — disappears
   if synthesis lives in a SQLite event log.

activegraph is parked as a possible v2 substrate, especially for the
audit/replay story. See [[activegraph]] for the offline quickstart
notes.

## Related

- [[llm-evaluation]] — how either runtime would be benchmarked.
- [[howtoeval]] — eval philosophy that applies regardless of substrate.
