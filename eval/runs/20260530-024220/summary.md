# Eval run 20260530-024220

## Aggregate score (correct facts / total facts)

| Model | wiki | rag |
|---|---|---|
| claude-sonnet-4-6 | 23/23 (100%) | 9/23 (39%) |
| gpt-5-mini | 23/23 (100%) | 9/23 (39%) |

## Per-question detail

### q1-msme-vs-retail

> Across H1 FY25 through 9M FY26, which segment has consistently grown faster YoY: MSME advances or Retail advances? Cite the YoY figures for at least three of the six periods.

| Agent | Model | Score | Latency |
|---|---|---|---|
| wiki | claude-sonnet-4-6 | 3/3 | 14.42s |
| wiki | gpt-5-mini | 3/3 | 19.19s |
| rag | claude-sonnet-4-6 | 0/3 | 132.73s |
| rag | gpt-5-mini | 0/3 | 41.93s |

### q2-pat-deceleration

> What happened to industry PAT growth between FY25 and FY26 according to the BCG roundups, and what was the proximate cause?

| Agent | Model | Score | Latency |
|---|---|---|---|
| wiki | claude-sonnet-4-6 | 4/4 | 19.35s |
| wiki | gpt-5-mini | 4/4 | 10.14s |
| rag | claude-sonnet-4-6 | 0/4 | 9.59s |
| rag | gpt-5-mini | 0/4 | 16.78s |

### q3-roa-by-category-9m-fy26

> For 9M FY26, which bank category had the highest ROA and which had the lowest, in percent? Show the full ROA tree (NIM, fee income, opex, credit costs) for both.

| Agent | Model | Score | Latency |
|---|---|---|---|
| wiki | claude-sonnet-4-6 | 4/4 | 12.47s |
| wiki | gpt-5-mini | 4/4 | 13.92s |
| rag | claude-sonnet-4-6 | 4/4 | 10.41s |
| rag | gpt-5-mini | 4/4 | 17.27s |

### q4-rate-cycle-context

> By how many basis points has RBI cut the repo rate since February 2025, and what was the total liquidity infusion through CRR reduction in 2025? Why did this not translate fully into bank margin expansion?

| Agent | Model | Score | Latency |
|---|---|---|---|
| wiki | claude-sonnet-4-6 | 5/5 | 19.72s |
| wiki | gpt-5-mini | 5/5 | 11.98s |
| rag | claude-sonnet-4-6 | 5/5 | 15.75s |
| rag | gpt-5-mini | 5/5 | 12.4s |

### q5-casa-trend

> Describe the trend in industry CASA ratio from H1 FY25 to 9M FY26. Provide period-by-period numbers and a one-sentence explanation of what is driving it.

| Agent | Model | Score | Latency |
|---|---|---|---|
| wiki | claude-sonnet-4-6 | 7/7 | 10.06s |
| wiki | gpt-5-mini | 7/7 | 10.01s |
| rag | claude-sonnet-4-6 | 0/7 | 8.9s |
| rag | gpt-5-mini | 0/7 | 14.94s |