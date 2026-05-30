# Log

Append-only. Newest entries at the top.

---

## 2026-05-30 — Ingest + applied: Shankar qual-analysis -> eval-failure-taxonomy

- Read https://www.sh-reya.com/blog/ai-qual-analysis/ (Shreya
  Shankar, May 2026). Six-condition experiment on grounded-theory
  coding by Claude Sonnet over 451 tweets. Headline: "agents can do
  the mechanical parts of qualitative analysis fast, but they have
  no taste."
- Created `raw/shankar-qual-analysis.md` and
  `wiki/shankar-qual-analysis.md`.
- Applied the method to `eval/runs/20260530-033125/results.jsonl`:
  - Read all 31 imperfect cleanly-judged cells by hand. Open coded
    23 raw labels, axial-collapsed to 8 categories.
  - Wrote `wiki/eval-failure-taxonomy.md` with codes F1-F8, cell
    citations, and severity tags.
- Findings:
  - 23 of 23 RAG failures are retrieval-driven (F1-F4).
  - Half of wiki failures are not the wiki's fault (F5 prompt
    brevity, F7 judge paraphrase mismatch).
  - One genuine wiki gap (F8): FY25 NIM YoY -11 bps belongs in
    wiki/banking-sector-roundup.md and isn't there.
- Action items in the taxonomy: tighten judge before adding more
  questions; tighten wiki agent prompt; patch the FY25 NIM gap;
  don't fix RAG chunking yet (the gap is the experimental finding).
- Updated `index.md`.

## 2026-05-30 — Scaled to 50 questions; OpenRouter ran out mid-run

- Authored 45 more questions, total 50 (24 lookup, 26 synthesis,
  173 facts).
- Hardened harness:
  - `eval/_models.py`: 4-attempt retry with exp backoff on
    IncompleteRead / RemoteDisconnected / 429 / 5xx.
  - `eval/run.py`: writes results.jsonl line-by-line with flush; new
    --resume flag skips already-graded cells.
- Run `eval/runs/20260530-033125/`, GPT-5 mini only.
  - All 100 answer cells succeeded.
  - Judge calls started failing at q19 with HTTP 402 "more credits
    needed" -> OpenRouter balance ran out (account usage $1.08 total).
  - Of 50 wiki rows, 36 were judged, 14 returned JUDGE_ERROR with
    correct/total = 0/X, polluting the aggregate.
  - Apparent headline: wiki 110/173 (64%) vs. rag 32/173 (18%) on
    GPT-5 mini, but 14 of the 0/X wiki rows are false-zeros caused by
    judge failures, not by wrong answers (verified manually on q39 et
    al. — answers were correct).
  - Real scores require a regrade once OpenRouter is topped up.
- Added `eval/rejudge.py`: re-grades only rows with JUDGE_ERROR,
  preserves correctly-graded rows, defaults to a cheap judge model
  (gemini-2.5-flash). Backups results.jsonl to .pre-rejudge first.
- Added `eval/resummary.py`: rebuilds summary.md from results.jsonl.

## 2026-05-30 — First eval run: wiki 100% vs. RAG 39%

- Built smallest end-to-end eval harness:
  - `eval/golden/questions.jsonl`: 5 hand-authored questions over the
    BCG corpus (2 lookup, 3 cross-period synthesis).
  - `eval/agents/wiki_agent.py`: stuffs all `wiki/*.md` (~24 KB) into
    the system prompt, asks for cited answer.
  - `eval/agents/rag_agent.py`: chunks 6 PDFs (331 chunks @ 350 words),
    local sentence-transformers MiniLM-L6 embeddings, top-8 retrieval.
  - `eval/judge.py`: per-fact LLM-as-judge YES/NO grading.
  - `eval/run.py`: questions × agents × models, writes summary.md.
- Switched from per-vendor keys to OpenRouter (single key satisfies the
  Anthropic + OpenAI requirement). `eval/_models.py` uses urllib only.
- Switched embeddings from Voyage to local sentence-transformers
  (sentence-transformers/all-MiniLM-L6-v2). No embedding API key needed.
- Run `eval/runs/20260530-024220/`:
  - Wiki agent: 23/23 (100%) on Sonnet 4.6 AND on GPT-5 mini.
  - RAG baseline: 9/23 (39%) on both models.
  - RAG matched wiki on the 2 single-source questions, scored 0/X on
    all 3 cross-period synthesis questions. Failure mode confirmed
    PITCH.md's prediction.
- Updated `PITCH.md`: replaced "to be filled" headline table with the
  actual numbers and a "where the gap comes from" section. Added a
  "failures we publish" note flagging that even 100% answers had subtle
  hallucinations the per-fact judge didn't catch.

## 2026-05-30 — Pulse pilot run on 9M FY26 (46 pages, 46 credits)

- Ran `scripts/parse_pdf.py raw/banking-sector-roundup-9mfy26.pdf
  --pages 3-48` (one off-by-one error first: deck is 48 pages, not 49).
- Wrote `raw/parsed/banking-sector-roundup-9mfy26.parsed.md` (76 KB).
- Updated `wiki/indian-banking-fy25-fy26.md` with two new sections,
  both citing the parsed source:
  - Section 8: full ROA-tree table by bank category (Industry / PSU /
    Pvt-New / Pvt-Old / SFB) for 9M FY26 with 9M FY25 comparison.
    Cleanly extracted from the parser output.
  - Section 9: rate-cycle setup — RBI 125 bps cuts since Feb 2025,
    100 bps CRR reduction, ~₹2.5 lakh crore liquidity, sticky deposit
    rates as the proximate cause of NIM compression.
- Created `raw/pulse.md` and `wiki/pulse.md` to document the
  dependency, with quality notes on what Pulse is good and bad at
  (good: prose, structured tables; bad: infographics, charts).
- Updated `index.md` — added `parsed/` entry and `pulse.md`,
  `wiki/pulse.md`.

## 2026-05-30 — Pulse parser wired in (.env, scripts/parse_pdf.py)

- User provided a Pulse API key. Verified vendor (https://docs.runpulse.com),
  base URL `https://api.runpulse.com`, auth header `x-api-key`.
- Probed `/extract` with empty body to verify the key: HTTP 400 "No file
  or URL provided" -> auth passes, key is valid.
- Created `.gitignore` (was missing) before writing `.env`. Confirmed
  `git check-ignore` blocks `.env` and allows `.env.example`.
- Wrote `.env` (gitignored) with PULSE_API_KEY and `.env.example`
  (tracked, blank value) as the public template.
- Added `scripts/parse_pdf.py`: stdlib-only, ~80 LOC. Multipart upload,
  optional `--pages`, follows Pulse's `is_url` large-response handoff,
  writes markdown to `<pdf>.parsed.md` or `--out`.
- Pilot: parsed pages 3-4 of `banking-sector-roundup-9mfy26.pdf` for 2
  credits. Output written to /tmp/pulse-test.md (not committed).
- Quality verdict: visual snapshot grids (page 2) come out worse than
  manual transcription -- mangled colspans, currency glyphs leaked.
  Prose-heavy interior pages (page 4 summary) are clean and surface
  new claims (e.g., ROA 1.39% -> 1.33%, NIM -21 bps tied to deposit
  competition). Parser should be aimed at pages 3+, not page 2.
- Note on workspace state: user has parallel work in `.activegraph/`,
  `agpack/`, `naive/`, `playground/`, and `*.py` files at repo root
  that I did not create and have not touched.

## 2026-05-30 — Ingest: BCG Banking Sector Roundup, 6 PDFs

- Moved 6 PDFs from repo root into `raw/`: BCG Banking Sector Roundup
  decks for H1 FY25, 9M FY25, FY25, Q1 FY26, H1 FY26, 9M FY26 (~300
  pages, ~17 MB total).
- Identified publisher: Boston Consulting Group. Each deck covers 36–37
  Indian banks (12 PSU, 10 Private-New, 10 Private-Old, 4–5 SFBs).
- Read page 2 ("industry snapshot") of every deck. Did NOT read pages
  3+ — flagged as open threads in the wiki.
- Created `raw/banking-sector-roundup.md` — series notes, full
  cross-period table including YoY deltas, methodology caveats.
- Created `wiki/banking-sector-roundup.md` — summary page with the
  cross-period table and a one-paragraph read.
- Created `wiki/indian-banking-fy25-fy26.md` — concept page with seven
  cross-period themes (volume vs. profit, NIM compression, non-interest
  income carry, CASA bleed, GNPA improvement, MSME outpacing retail,
  ROA softening) and open threads for follow-up reading.
- Updated `index.md` with the new sources and pages.

## 2026-05-30 — Ingest: activegraph (with hands-on quickstart)

- User asked about `activegraph`. Verified the package exists on PyPI
  (1.0.5.post2, uploaded 2026-05-20) and on GitHub
  (yoheinakajima/activegraph, created 2026-05-16, alpha, Apache-2.0).
- Created throwaway venv at `/tmp/activegraph-sandbox` (uv, Python 3.12),
  installed `activegraph` (7-package dep tree), ran `activegraph
  quickstart` against bundled fixtures: 3 companies, 671 events, 103 LLM
  requests, ~25s wall clock, fully offline. Output persisted to
  `sqlite:////tmp/activegraph_quickstart/quickstart_demo_run.db`.
- Did NOT run `--interactive` (writes scaffolding to CWD, prompts user-
  facing). Left for the user to drive.
- Added `raw/activegraph.md` (capabilities, packs, quickstart numbers,
  diff vs. wiki pattern).
- Added `wiki/activegraph.md` summary.
- Added `wiki/agent-runtimes.md` concept page comparing the LLM-wiki
  pattern with activegraph and recording the v1 decision: stay on the
  wiki pattern, park activegraph as possible v2.
- Updated `index.md`.

## 2026-05-30 — Scope locked: PITCH.md

- Created `PITCH.md` at repo root. Vertical: banking / corp finance.
  Headline: "wiki-grounded agent beats RAG on Vals CorpFin v2 / Finance
  Agent v2." Failures published openly per howtoeval.
- Non-goals recorded: no SaaS, no framework, no embeddings in the wiki
  agent unless link graph proves insufficient.
- Roadmap: freeze corpus -> build RAG baseline -> compile wiki -> runner
  -> 10 golden cases -> publish. TaxEval is a stretch follow-up.

## 2026-05-30 — Ingest: Vals AI + howtoeval.com

- Added `raw/vals-ai.md` (https://www.vals.ai/home) — independent AI model
  benchmarking platform. Captured benchmark domains, models tracked,
  offerings, and a Vals Index snapshot (Claude Opus 4.8 leading at 70.17%).
- Added `raw/howtoeval.md` (https://www.howtoeval.com/) — Ben Hylak's May
  2026 guide to evaluating AI agents. Captured the benchmark-maxxing vs.
  floor-raising frame, pre-ship practices, offline-eval stance, production
  loop, and Raindrop / Raindrop Workshop vendor context.
- Created `wiki/vals-ai.md` and `wiki/howtoeval.md` summary pages.
- Created `wiki/llm-evaluation.md` concept page tying both sources together
  and cross-linking to existing `raw/rag.md`.
- Updated `index.md`.

## 2026-05-29 — Wiki scaffolded

- Created `AGENTS.md` (schema), `index.md` (catalog), `log.md` (this file).
- Created empty `raw/` and `wiki/` directories.
- Reference: Karpathy's LLM-wiki gist
  (https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
- No sources ingested yet.
