---
title: Pulse (document parser)
type: summary
sources:
  - raw/pulse.md
  - https://docs.runpulse.com
updated: 2026-05-30
---

# Pulse

Document-intelligence API used in this project to parse the BCG banking
PDFs into markdown. See [[banking-sector-roundup]] for the corpus and
[[indian-banking-fy25-fy26]] for claims sourced from parsed output.

## In this project

- Wrapper script: `scripts/parse_pdf.py` (stdlib-only Python).
- Key: `PULSE_API_KEY` read from `.env` (gitignored). Template in
  `.env.example`.
- Outputs: `raw/parsed/<deck>.parsed.md`, separate from the PDF
  source.

## API quick facts

- Base URL: `https://api.runpulse.com`
- Auth: header `x-api-key`
- Main endpoint: `POST /extract` — multipart `file=` or JSON `file_url`.
- Optional `pages` range (1-indexed, inclusive). Off-by-one if you go
  past the end (`REQ_006`).
- Returns `{markdown, page_count, credits_used, ...}` for small docs;
  switches to a 1-hour signed URL at ~70 pages or 5MB.

## When to use it

Good:
- Prose-heavy interior pages.
- Structured numeric tables (e.g., the BCG ROA tree by bank category
  came out clean).

Avoid:
- Infographic / dashboard pages with tile layouts — manual transcription
  from the rendered image is more accurate.
- Chart-only pages — numeric labels are extracted but lose their
  category alignment.

## Cost so far

48 credits used on this project: 2 (test, page 3-4 of 9M FY26) + 46
(full pages 3-48 of 9M FY26).

## Related

- [[banking-sector-roundup]] — primary downstream consumer.
- [[indian-banking-fy25-fy26]] — concept page extended with claims
  recovered from Pulse output (sections 8 and 9).
