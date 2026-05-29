# LLM Wiki — Schema

This repo is an **LLM-maintained wiki** following the pattern in
https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f.

The agent (you) is the librarian. The human curates **sources**; you maintain
the **wiki**. Synthesis is compiled once into durable pages, not rediscovered
on each query.

## Layout

```
raw/        # immutable sources — you READ these, never edit
wiki/       # your pages — entities, concepts, summaries (markdown, interlinked)
index.md    # catalog of what's in raw/ and wiki/ — keep current
log.md      # append-only chronological log of ingests, queries, lints
AGENTS.md   # this file — the schema
```

## Conventions

- **Files**: kebab-case `.md`. One entity / concept / source-summary per file.
- **Links**: `[[wiki/page-name]]` for internal, full URL for external.
  Unresolved `[[name]]` links are fine — they mark pages worth writing.
- **Frontmatter** on every wiki page:
  ```yaml
  ---
  title: ...
  type: entity | concept | summary | log
  sources: [raw/foo.md, https://...]   # what this page draws from
  updated: YYYY-MM-DD
  ---
  ```
- **Citations**: every non-trivial claim cites a source — either a `raw/` file
  or an external URL. No uncited assertions.
- **Tone**: terse, factual, structured. This is a reference, not an essay.

## Operations

### Ingest
Triggered when a new source lands in `raw/` (or the user pastes one).
1. Read the source.
2. Write or update one summary page in `wiki/` for it.
3. Update related entity / concept pages — typically 5–15 touched per ingest.
4. Update `index.md`.
5. Append a dated entry to `log.md` (what was ingested, what changed).

### Query
The user asks a question.
1. Answer from `wiki/` first; fall back to `raw/` only when the wiki is thin.
2. Cite sources inline.
3. If the answer is non-trivial and reusable, file it back into `wiki/`
   (new page or update existing) and log it.

### Lint
Run periodically (or when asked).
1. Find contradictions across pages.
2. Find stale claims (frontmatter `updated` far behind newer sources).
3. Find orphans (no inbound links) and dead `[[links]]`.
4. Suggest merges / splits / cross-references.
5. Report findings; apply fixes only on user confirmation.

## Default behavior

- Prefer **updating existing pages** over creating new ones.
- When in doubt about scope, **ask the user**, then save the answer here so
  you don't ask twice.
- Never edit `raw/`. Never silently delete wiki pages — propose first.
