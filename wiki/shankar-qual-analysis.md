---
title: Shankar — Agent-Assisted Qualitative Analysis
type: summary
audience: internal
sources:
  - raw/shankar-qual-analysis.md
  - https://www.sh-reya.com/blog/ai-qual-analysis/
updated: 2026-05-30
---

# Shankar: Agent-Assisted Qualitative Analysis

Shreya Shankar, May 2026. Six-condition experiment with Claude Sonnet
via Anthropic Agent SDK on 451 tweets, doing grounded-theory coding.

## Headline

Agents can do the mechanical parts of qualitative analysis fast, but
they have no taste. The right framing isn't full automation; it's
where human taste composes with agent scale.

## Why this is in this wiki

Two reasons:

1. **Failure-mode analysis on agent traces is itself qualitative
   analysis.** Inspecting `eval/runs/*/results.jsonl` to figure out
   *why* an agent got a question wrong is exactly the task Shankar
   studies. Her findings are predictions for what happens if we point
   an agent at our results.
2. **Eval literature triangulation.** Sits adjacent to
   [[howtoeval]] (Hylak: golden cases, code-native harness) and
   [[llm-evaluation]] (benchmark vs. floor raising). Shankar is the
   *understanding what your agent does wrong* layer; Hylak is the
   *measuring whether it works* layer.

## Concrete failure modes (verbatim)

1. **Paraphrasing instead of analyzing** — code count correlated with
   input length at ρ=0.81.
2. **No code reuse** — 93.8–100% of codes used exactly once.
3. **Premature stopping** — 6% to 68% coverage of the 451 tweets.
4. **Skipping hard cases** — empty code lists, "unclear mixed message"
   dismissals.
5. **Bad orchestration** — multi-agent timeouts caused fallback to
   keyword/substring matching.
6. **Feedback loop failures** — overfit to one comment, or forget
   feedback within a round.

## Discipline she imposes (and we should too)

- Reuse codes. New code only when nothing existing fits.
- Falsifiable categories. "Reliability issues" is not a code; it's a
  feeling.
- Don't dismiss hard cases. The hard cases are the finding.
- Surface provenance, uncertainty, disagreement, stabilization,
  evidence — not just labels.

## Applied in this repo

- [[eval-failure-taxonomy]] — hand-coded failure modes for the
  20260530-033125 eval run, following Shankar's reuse-and-falsifiable
  discipline. 23 raw codes collapsed to 8 axial categories, each
  citing the specific cells it covers.

## Open threads

- We have not run an agent at the failure-coding step. We did it
  by hand. Worth trying *once* the corpus reaches a size where hand
  coding is infeasible — and validating Shankar's predictions on
  this corpus.
- The "redefine saturation around human learning" suggestion is
  abstract; what does it mean in a 50-question eval?
