---
title: Eval Failure Taxonomy (run 20260530-033125)
type: concept
sources:
  - eval/runs/20260530-033125/results.jsonl
  - https://www.sh-reya.com/blog/ai-qual-analysis/
  - raw/howtoeval.md
updated: 2026-05-30
---

# Eval Failure Taxonomy

Hand-coded analysis of every imperfect cell in the 50-question eval run
on GPT-5 mini. Method: open coding on each failed cell, then axial
grouping into the ~7 categories below. The point is to turn a single
score (wiki 64%, RAG 18%) into a diagnosis of *what failed and why*.

Following [[shankar-qual-analysis]]: codes are deliberately reused
across cells, named to be falsifiable (every code lists which cells
fall under it), and grounded in *what the agent actually did* rather
than what it should have done.

## Inputs

- 100 answer cells (50 questions × 2 agents × 1 model = GPT-5 mini)
- 72 cleanly judged cells; 28 hit OpenRouter HTTP 402 mid-run and are
  excluded as `JUDGE_ERROR` rather than agent failure.
- 31 imperfect cells coded below: 8 wiki, 23 RAG.

## Codes (axial)

### F1. retrieval-missed-target-period (RAG only, 16 cells)

Top-k retrieval returned chunks from the wrong period of the BCG
series, or from generic/cover pages, leaving the agent unable to
answer for the period asked. Failure manifests as an honest "I cannot
find X in the provided passages" answer.

Cells: q5, q6, q7, q11, q12, q14, q15, q21, q22, q26, q27, q29
(partial), q31, q32, q34, q36.

This is the dominant RAG failure mode. The information *exists in the
PDF corpus*; the embedder just didn't surface it for that question.
The wiki agent doesn't have this failure mode because all six
periods are pre-compiled into the same markdown page.

### F2. rag-hallucination-on-empty-context (RAG only, 1 cell)

When retrieval found nothing relevant, the agent fabricated a plausible
number rather than refusing.

Cells: q33 — answered "cost-to-income ratio was about 50% in H1 FY25
and remained about 50% in 9M FY26" against actual values of 47.9% and
48.3%. Cited two pages that don't contain the figure.

Distinct from F1 because the agent didn't refuse; it produced a wrong
answer with confident-looking citations.

### F3. rag-empty-refusal (RAG only, 6 cells)

Agent returned an entirely empty string. System prompt asks for an
explicit "not in passages" statement when the data is absent. GPT-5
mini sometimes outputs nothing instead.

Cells: q9, q25, q30, q31, q34, q36.

Probably a model artifact rather than a logic failure. Worth flagging
because empty answers score 0 on every fact and inflate RAG's loss.

### F4. rag-reasoning-slip-on-retrieved-data (RAG only, 1 cell)

Retrieval succeeded; reasoning didn't.

Cells: q28 — retrieved the correct "ROA softened to 1.33% in 9M FY26"
chunk, then characterized the trajectory as "not monotonic (a decline
followed by a small increase)" by treating 1.30% and 1.33% as
distinguishable. The wiki's pre-compiled table shows ROA at 1.3% for
every period from FY25 onward; the chunk-level number is more
precise but the trajectory call is wrong.

### F5. answer-stops-short (wiki, 4 cells)

Agent gave a correct headline answer but didn't volunteer the
secondary fact the question asked for. Reflects a brief-answer style
in the wiki agent's prompt rather than missing knowledge.

Cells: q8 (got GNPA 1.9%, didn't add the -54 bps YoY also in the
wiki), q2 (got the +16-20%→+3-6% PAT deceleration, didn't quote NII
+2-3% vs +8-10%), q29 (got the NII deceleration numbers, didn't name
NIM compression as the cause), q34 (computed H1 FY26 deposits +10%
YoY, didn't separately quote H1 FY25 +12%).

Fix is on the prompt or judge side, not the wiki: the data was there.

### F6. wiki-coverage-blind-spot (wiki, 2 cells)

Agent claimed the wiki didn't contain a figure that the wiki *does*
contain. Pattern: the agent over-trusts a summary range note and
doesn't scan the table-row YoY values.

Cells: q6 (said "exact Q1 FY26 YoY figure is not in the wiki" but
banking-sector-roundup.md row "Deposits YoY" includes Q1 FY26: +12%),
q19 (cited the right month for the RBI stance shift but the judge
marked the second fact as missed because the answer paraphrased
"signals data dependence" as "marked a turn away from a prolonged
pause" — see F7).

### F7. judge-paraphrase-miss (cross-cutting, ≥3 cells)

Per-fact judge returned NO when the answer asserted the fact in
different words. Numbers are graded strictly; prose paraphrases are
not. This is a failure of the *grader*, not the agent.

Cells: q19 wiki ("data dependence" paraphrase), q29 wiki ("fell
sharply" implies but doesn't name compression), q12 wiki (computed
+21.9% from absolutes; expected +17% — agent's derivation is
internally consistent but doesn't match the published rounded figure;
arguably a real miss, not a paraphrase one).

Expected behaviour per [[howtoeval]]'s "floor raising": the judge
should be the next thing improved before adding more questions.

### F8. wiki-data-gap (wiki, 1 cell)

Wiki page intentionally records "n/a" for a metric (FY25 NIM YoY
delta), forcing the agent to either compute it from earlier data or
say it isn't in the wiki. Agent gave the wrong derivation.

Cells: q9 (expected "11 bps YoY decline" — that exact figure is in
raw/banking-sector-roundup.md but the wiki concept page only
mentions the FY26 -21 to -27 bps range).

This one is a real gap the wiki should fix on the next ingest pass.

## Counts

| Code | Cells | Agent | Severity |
|---|---:|---|---|
| F1 retrieval-missed-target-period | 16 | rag | high |
| F2 rag-hallucination | 1 | rag | high |
| F3 rag-empty-refusal | 6 | rag | model artifact |
| F4 rag-reasoning-slip | 1 | rag | low |
| F5 answer-stops-short | 4 | wiki | prompt-fixable |
| F6 wiki-coverage-blind-spot | 2 | wiki | prompt-fixable |
| F7 judge-paraphrase-miss | ≥3 | judge | judge-fixable |
| F8 wiki-data-gap | 1 | wiki | wiki-fixable |

## Read-out

The wiki vs. RAG gap is real but its *shape* is more interesting than
its size:

- **23 of 23 RAG failures are retrieval-driven** (F1+F2+F3+F4). The
  baseline does not lose because of model capability; it loses
  because chunked top-k retrieval over visually-heavy slide PDFs
  doesn't surface the right page for cross-period questions.
- **Half of wiki failures are not the wiki's fault** (F5 prompt
  brevity, F7 judge paraphrase mismatch). Fix the prompt and judge
  before adding questions.
- **One genuine wiki gap** (F8). The +11 bps FY25 NIM YoY decline
  belongs in `wiki/banking-sector-roundup.md` and isn't there yet.

## Discipline notes ([[shankar-qual-analysis]])

Watching for the failure modes Shankar catalogues:

- **Code reuse:** F1 was applied to 16 cells, F3 to 6, F5 to 4. Did
  *not* invent a unique code per cell. (Open coding produced 23 raw
  labels; axial collapsed them to 8.)
- **Falsifiability:** every code names specific cells. "Reliability
  issue" would not count.
- **Skipping nothing:** every imperfect cleanly-judged cell appears
  under exactly one code. The 28 JUDGE_ERROR cells are excluded
  explicitly (not silently dropped).
- **Avoid paraphrase:** codes name what the agent *did*
  (retrieval-missed-target-period, empty-refusal,
  reasoning-slip-on-retrieved-data), not what it failed to do.

## Action items for the next iteration

1. **Strengthen the judge** before adding more questions (F7). Either
   tighten the YES/NO prompt with "paraphrase counts" examples, or
   switch to a numeric-tolerance grader for numeric facts.
2. **Tighten the wiki agent prompt** to volunteer secondary facts
   when the question asks for them (F5, F6).
3. **Patch wiki/banking-sector-roundup.md with FY25 NIM YoY decline
   (-11 bps)** (F8).
4. **For RAG**: don't bother fixing chunking yet. The retrieval gap
   is real and that's the experimental finding. If the gap closes
   under better retrieval, that becomes the v2 comparison.

## Related

- [[shankar-qual-analysis]] — methodology source.
- [[llm-evaluation]] — concept page; this taxonomy is the
  "floor-raising" half.
- [[howtoeval]] — pre-ship golden cases; this run is one of those.
- [[banking-sector-roundup]] — the source corpus.
