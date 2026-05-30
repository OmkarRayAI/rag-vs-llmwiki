# Social copy

Drafts for sharing the repo. Not committed to a single voice — pick by audience.

## Pre-flight

- Attach `docs/charts/score_by_difficulty.png` to anything visual.
- Don't tag Karpathy, Anthropic, OpenAI, or other large accounts.
- Don't post from a fresh account; build credibility on this one's history.
- The maximalist drafts will draw RAG-optimization replies ("did you try a reranker?"). The README discloses this; the captions don't. If you can't link to the README in the same post, prefer measured.

---

## Twitter — measured (recommended)

### Option A — table-first

> Built the LLMWiki pattern (Karpathy's gist) on real banking PDFs and benchmarked it head-to-head against vanilla RAG.
>
> Same model. Same 6 PDFs. Same 50 questions. Only retrieval differs.
>
> Wiki: 86% / 95% (lookup / synthesis)
> RAG: 56% / 11%
>
> 100% of RAG's failures were retrieval-driven.
>
> Repo + every wrong answer, coded:
> github.com/OmkarRayAI/rag-vs-llmwiki

### Option B — failure-quote

> Asked vanilla RAG: *"Show CASA ratio across these 6 BCG banking decks."*
>
> RAG: *"I cannot find period-by-period CASA values."*
>
> The values were in the corpus. Top-k just didn't surface them.
>
> Pre-compiled wiki: had all 6 in a single table. 95% on synthesis vs RAG's 11%.
>
> github.com/OmkarRayAI/rag-vs-llmwiki

---

## Twitter — maximalist (higher views, higher pushback)

### Option C — punchy

> RAG dies on cross-period synthesis. 11% on questions like *"how did X change across these 6 reports?"*
>
> Pre-compiled markdown wiki on the same corpus: 95%.
>
> Same model. Same PDFs. Only the retrieval strategy changes.
>
> Stop chunking. Start writing.
>
> github.com/OmkarRayAI/rag-vs-llmwiki

### Option D — meme-shaped

> Karpathy was right.
>
> Wiki agent vs vanilla RAG, same 6 PDFs, same questions, same model:
> 94% vs 11% on cross-period synthesis.
>
> [chart]
>
> github.com/OmkarRayAI/rag-vs-llmwiki

---

## Twitter — thread, credibility-first (RECOMMENDED)

Updated 2026-05-30 with the fully-judged dataset (Gemini 2.5 Flash
re-graded the q19+ cells the original judge couldn't reach). Numbers
match `eval/runs/20260530-033125/results.jsonl` and the chart at
`docs/charts/score_by_difficulty.png`.

### Tweet 1 — hook (with N upfront)

> Tested Karpathy's "LLM wiki" idea against vanilla RAG on real
> banking PDFs.
>
> 6 BCG decks, 50 hand-authored questions, GPT-5 mini both sides.
>
> Wiki 145/173 facts (84%). RAG 48/173 (28%).
>
> Why, and what failed: 👇
>
> github.com/OmkarRayAI/rag-vs-llmwiki

### Tweet 2 — chart + the asymmetry disclosed

> [attach `docs/charts/score_by_difficulty.png`]
>
> The setup, fairly stated: the wiki (24 KB markdown) fits whole
> in the system prompt. RAG retrieves top-8 chunks (~2 KB).
>
> Same model, same source PDFs, but the wiki agent gets ~8x more
> context than RAG. That asymmetry IS the wiki pattern's bet.

### Tweet 3 — the diagnosis

> Where does RAG lose? Cross-period synthesis: wiki 89% vs RAG 14%.
>
> Hand-coded every failure (Shankar's qual-analysis discipline).
> Every RAG miss on synthesis was retrieval-driven — the data WAS
> in the corpus. Top-k just didn't pull six periods together.

### Tweet 4 — the failure quote (most retweetable)

> Sample failure. q5: *describe the CASA ratio trend across all 6
> periods.*
>
> RAG: *"I cannot provide period-by-period industry CASA ratio
> numbers because the provided passages do not contain those values."*
>
> The values were indexed. Just not retrieved together.
> Wiki had all 6 in a pre-built table. Lookup.

### Tweet 5 — caveats I'm not hiding

> Caveats:
>
> • One model. One corpus. ONE-METHOD baseline (vanilla top-k, no
>   reranker / hybrid / query rewriting).
> • Judge is split: GPT-5 mini graded q1–q18, Gemini 2.5 Flash
>   graded q19–q50 (original judge ran out of credits mid-run).
>   Switching judges between cells is real noise.
> • The wiki was hand-built. This tests whether HAVING one helps,
>   not whether an LLM can maintain one (Karpathy's separate claim).

### Tweet 6 — the actual point

> The bet: synthesis is the work. RAG re-does it on every query.
> A wiki does it once.
>
> Computers are cheap enough now to maintain "once" forever, with
> no human bookkeeping.
>
> Repo: harness, all 50 Qs, every answer, every failure hand-coded:
> github.com/OmkarRayAI/rag-vs-llmwiki

---

## Twitter — thread, original (more punch, less defended)

### Tweet 1 — hook

> Spent a weekend testing whether Karpathy's LLM-wiki idea actually beats RAG on real corp-fin PDFs.
>
> Built both. Same model. Same 6 BCG banking decks. 50 hand-authored questions.
>
> Result: wiki 95% / RAG 11% on cross-period synthesis questions.
>
> Thread + repo 👇

### Tweet 2 — chart

> [attach `docs/charts/score_by_difficulty.png`]
>
> Lookup ("what was Q1 FY26 GNPA?"): RAG 56%, wiki 86%.
>
> Synthesis ("how did GNPA change across all 6 periods?"): RAG 11%, wiki 95%.

### Tweet 3 — diagnosis

> Why does RAG lose so badly on synthesis? I hand-coded every wrong answer.
>
> 100% of RAG's failures were retrieval-driven. Top-k over slide PDFs couldn't find the right page for cross-period questions — even though the data was in the corpus.

### Tweet 4 — failure quote (most retweetable)

> Most damning example. q5: *describe the CASA ratio trend across 6 periods.*
>
> RAG: *"I cannot find period-by-period CASA values in the provided passages."*
>
> The values were in the index. The retriever just didn't surface them. Wiki had all 6 in a pre-built table.

### Tweet 5 — caveats (credibility builder)

> Caveats I'm not hiding: one model (GPT-5 mini), one corpus, judge ran out of credits at q19 (14 cells excluded). Half my "wiki failures" were judge paraphrase mismatches, not real misses.
>
> All 31 imperfect cells coded with citations.

### Tweet 6 — close

> The bet: synthesis is the work. RAG re-does it on every query. The wiki does it once.
>
> Computers are now cheap enough to maintain "once" forever.
>
> Repo, harness, every answer, every failure: github.com/OmkarRayAI/rag-vs-llmwiki

---

## LinkedIn — credibility-first (RECOMMENDED)

### Option L0

> Andrej Karpathy proposed an alternative to RAG: instead of re-retrieving and re-synthesizing context for every query, have an LLM agent maintain a Wikipedia-style markdown wiki once. Future queries read the wiki.
>
> I built it on a real corp-fin corpus to see whether the idea holds up.
>
> **Setup**
>
> 6 BCG Banking Sector Roundup PDFs (~300 pages, FY25 → 9M FY26). I hand-built the wiki — that's the experiment, not a product. Then I built a vanilla RAG baseline on the same PDFs (350-word chunks, MiniLM-L6 embeddings, top-8 retrieval — the textbook playbook). Authored 50 questions, ran both agents on GPT-5 mini, judged each expected fact YES/NO.
>
> **Result, full 50 questions, all 173 facts judged**
>
>  • Lookup ("what was Q1 FY26 GNPA?"): Wiki 72%, RAG 57%.
>  • Cross-period synthesis ("how did GNPA change across all 6 periods?"): Wiki 89%, RAG 14%.
>  • Aggregate: Wiki 145/173 facts (84%), RAG 48/173 (28%).
>
> **What I take from it**
>
> All 23 RAG failures were retrieval-driven. The model was honest — it said "I cannot find this in the passages" — but the data WAS in the corpus. Top-k just couldn't pull six periods of CASA ratio together for one query. The wiki had those tables pre-compiled, so synthesis questions reduced to lookups.
>
> The fair caveat: the wiki (24 KB) fits whole in the system prompt; RAG saw ~2 KB of retrieved chunks. That asymmetry IS the wiki pattern's bet — that you can pre-compile a small synthesized artifact instead of a large unsynthesized index.
>
> **What I'm not claiming**
>
> One model. One corpus. Fallible LLM-as-judge — at least 3 wiki "failures" were the judge marking paraphrases as NO. 14 cells got excluded as JUDGE_ERROR when OpenRouter ran out of credits mid-run. Every wrong answer is hand-coded into 8 categories with cell-level citations, following Shankar's qualitative-analysis discipline.
>
> The repo includes the harness, every question, every answer, every failure mode, charts, and reproduction in 3 commands:
> github.com/OmkarRayAI/rag-vs-llmwiki

---

## LinkedIn — original drafts (less defended)

### Option L1

> I spent the weekend testing a contrarian take on RAG.
>
> Andrej Karpathy proposed an alternative: instead of re-retrieving and re-synthesizing context for every query, have an LLM agent maintain a Wikipedia-style markdown wiki once. Future queries read the wiki.
>
> I built both — Karpathy's wiki pattern and standard top-k RAG — over the same 6 BCG Banking Sector Roundup PDFs, used the same model (GPT-5 mini), and ran 50 hand-authored questions through both.
>
> Results:
>  • Lookup questions: Wiki 86%, RAG 56%
>  • Cross-period synthesis: Wiki 94%, RAG 11%
>
> 100% of RAG's failures were retrieval-driven. The model was honest — it kept saying "I cannot find this in the passages" — but the data was in the corpus. Top-k retrieval just couldn't surface it for questions like "how did GNPA change across these six reports?"
>
> The wiki had those cross-period tables pre-compiled in markdown, so synthesis questions reduced to lookups.
>
> Caveats: one model, one corpus, fallible LLM-as-judge. I hand-coded all 31 wrong answers (Shankar's qualitative-analysis discipline) into 8 categories with cell-level citations. Half the "wiki failures" turned out to be judge paraphrase mismatches, not corpus problems.
>
> The repo includes the harness, every question, every answer, every failure mode, and reproduction in 3 commands:
> github.com/OmkarRayAI/rag-vs-llmwiki
>
> Most "AI + your docs" products today are RAG. This experiment isn't a verdict — but it suggests the synthesis layer (which RAG re-does on every query) is the actual work, and computers are now cheap enough to maintain it as a durable artifact.

## LinkedIn — short

### Option L2

> Tested Karpathy's "LLM wiki" pattern against vanilla RAG on the same 6 banking PDFs, same model, 50 hand-authored questions.
>
> Wiki: 95% on cross-period synthesis. RAG: 11%.
>
> 100% of RAG's failures were retrieval-driven — the data was in the corpus, top-k just didn't find it. The wiki pre-compiled the cross-period tables once, so synthesis became lookup.
>
> Repo, harness, every wrong answer hand-coded into a failure taxonomy: github.com/OmkarRayAI/rag-vs-llmwiki

---

## Replies you should expect (and have answers ready for)

- **"You didn't try a reranker / hybrid search / query rewriting."**
  Correct. The point of the baseline is "what does the textbook playbook
  buy you," not "is RAG fundamentally broken." See README caveats.

- **"50 questions is small. One model is small."**
  Correct. README discloses this. Next iteration: more questions, second
  model tier, second domain (tax).

- **"You hand-built the wiki — that's not the LLM doing it."**
  Correct. This experiment measures whether *having* a maintained wiki
  helps. Whether an LLM can maintain one is Karpathy's separate
  claim — not what this repo tests.

- **"Your judge is unreliable."**
  Yes. The failure taxonomy explicitly flags 3+ cells as judge
  paraphrase-miss (F7). Stricter rubric is action item #1.

- **"Which OpenRouter model exactly?"**
  `openai/gpt-5-mini` for both agents and the judge.
  See `eval/_models.py`.
