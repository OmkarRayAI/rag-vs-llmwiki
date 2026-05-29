# LLM Wiki (Karpathy)

Source: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

Andrej Karpathy proposes that an LLM agent can incrementally build and maintain
a persistent, interlinked markdown wiki, instead of relying on Retrieval-Augmented
Generation to retrieve from raw documents at each query.

Architecture has three layers:
- Raw sources, immutable, the LLM reads but never edits.
- The wiki, LLM-owned markdown files: summaries, entity pages, concept pages.
- The schema, a config file (CLAUDE.md or AGENTS.md) defining conventions.

Three operations: Ingest processes new sources and updates related pages.
Query synthesizes answers with citations. Lint checks for contradictions,
stale claims, orphans, and missing cross-references.

Key files: index.md as content catalog, log.md as chronological append-only timeline.

The pattern connects to Vannevar Bush's 1945 Memex vision. The missing
piece Bush could not solve was who does the bookkeeping. LLMs do it
tirelessly, so the wiki stays current.

Tooling tips reference Obsidian as the browsing UI, Obsidian Web Clipper
for sourcing, and git for version control.
