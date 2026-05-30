# How to Evaluate AI Agents (Ben Hylak)

Source: https://www.howtoeval.com/

A practical guide titled "How to evaluate AI agents," authored by Ben Hylak
and published May 2026. The guide is opinionated and pushes back against
heavy vendor tooling, arguing that evaluating agents "is not that complicated."

Target audience: engineering and product teams building AI agents that
operate autonomously or replace human workflows (banking agents, support
bots, AI doctors), as opposed to expert-augmentation tools.

Core framing distinguishes two strategies:
- Benchmark maxxing: chasing scores on public benchmarks.
- Floor raising: fixing real failures where reliability matters.

Pre-ship practices:
- Build 5 to 10 golden cases.
- Inspect full agent trajectories locally.
- Query the agent itself about its failures.

Offline evals favor code-aware test harnesses such as Vitest and pytest over
hosted dashboards. Examples cited include Sentry's vitest-evals and OpenAI's
"macro evals."

Production learning loop: Stumbles -> Issues -> Signals -> Experiments,
scaled by volume.

Iteration discipline:
- Reproduce bugs before fixing.
- Prune low-signal eval cases.
- Commit roughly 10 to 20 percent of dev time to evaluation.

Forward-looking thesis: as agents and models merge, "the harness collapses
into the model itself."

Author context: Hylak founded Raindrop, a production agent monitoring
platform, and Raindrop Workshop, a free open-source local testing tool. The
guide promotes both. Further-reading links point to work by Hamel Husain,
Anthropic, and OpenAI.
