# Exploring Agent-Assisted Qualitative Analysis (Shreya Shankar)

Source: https://www.sh-reya.com/blog/ai-qual-analysis/
Date: 2026-05-21
Author: Shreya Shankar (recently completed PhD; faculty offer accepted).

A blog post (explicitly "not a paper") reporting a six-condition
experiment in which Claude Sonnet, via the Anthropic Agent SDK,
attempts grounded-theory qualitative analysis on 451 tweets replying
to Sholto Douglas's question about when users reach for non-Claude
models. Conditions varied: methodology prompting on/off, level of
human-in-the-loop, single agent vs hierarchical or independent
multi-agent.

## Central claim

> Agents can do the mechanical parts of qualitative analysis fast,
> but they have no taste.

The research question is therefore not full automation but: where
does human taste compose with agent scale.

## What qualitative analysis is, in this framing

Reading messy unstructured data and figuring out what is interesting,
recurring, surprising, or important. The post explicitly extends this
to "mining agent logs for failure modes" — same task as
ethnography or user research.

Shankar uses grounded theory: open coding (short labels per passage),
axial coding (group codes into categories), selective coding (pick
core themes), with running memos.

## Why current agents struggle

Qual analysis is unverifiable. Unlike "did the code compile?", the
right analysis depends on researcher taste, audience, and goals.
Critically: "the evaluation criteria themselves evolve throughout the
workflow." Most agents assume stable objectives and converge
prematurely on fixed framings.

## Concrete failure modes she observed

1. **Paraphrasing instead of analyzing.** Code count correlated with
   tweet length at ρ=0.81. Longer input → more codes that mostly
   restate the input.
2. **No code reuse.** 93.8–100% of codes used exactly once across
   most conditions, despite the codebook being in context.
3. **Premature stopping.** Coverage ranged from 6% (exp3-hierarchical)
   to 68% (exp2-codes) of the 451 tweets.
4. **Skipping data.** Hard tweets got empty code lists or
   "unclear mixed message" dismissals. The hard cases are where the
   insight lives.
5. **Bad orchestration.** When multi-agent subagents timed out, the
   supervisor switched to Python keyword/substring matching —
   silently degrading to grep.
6. **Feedback loop failures.** Agents either overfit to single
   offhand human comments (one mention promoted to a top category)
   or forgot feedback within the same round.

## What it feels like to supervise

- Validating AI-proposed codes shifts the question from "what matters
  most?" to "can I justify deleting this?" Cognitive frame degrades.
- Vague categories ("Reliability and Trust") are unfalsifiable.
  > Vague codes are easy to believe and impossible to act on.
- Frustration came from low-leverage supervision, not wait time.

## Recommendations

- Don't preserve traditional workflows uncritically. Open/axial/memo
  were designed around human cognitive limits; agents have different
  ones.
- Try AI-proposed codes that humans rerank or weight, not approve.
- Consider simultaneous open + axial coding instead of sequential.
- Redefine theoretical saturation around human learning, not agent
  novelty (agents will keep producing new codes forever).
- Surface provenance, uncertainty, disagreement, stabilization,
  evidence in the UI.
- Preserve in-vivo coding — verbatim phrase highlighting felt
  natural.
- Scale to long documents, agent traces, multimodal data, million+
  corpora — places humans can't reach at all.

## Quotes

- "agents can do the mechanical parts of qualitative analysis fast,
  but they have no taste"
- "Vague codes are easy to believe and impossible to act on"
- "the evaluation criteria themselves evolve throughout the workflow"

## Position

Adjacent to but distinct from the eval-ops literature (Hylak,
Husain, Yan). Shankar comes from HCI / qualitative methods. She does
not cite those authors; her external references are the data-source
tweet and the Anthropic Agent SDK docs.
