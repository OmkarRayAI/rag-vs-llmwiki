# Pulse (runpulse.com)

Source: https://docs.runpulse.com/introduction
Marketing: https://www.runpulse.com/

Pulse is a document-intelligence API that extracts structured content
(markdown, tables, figures) from PDFs and similar documents using OCR,
layout detection, and vision models. Pitched as zero-shot and
document-type-agnostic.

## API surface (as observed 2026-05-30)

- Base URL: `https://api.runpulse.com`
- Auth: header `x-api-key`
- Endpoints: `/extract` (parse), `/split` (topic-based page grouping),
  `/schema` (apply a schema to extract structured JSON).

## /extract request shape

Multipart form:
- `file` (binary, required) OR `file_url` (string, required) — pick one.
- `pages` — 1-indexed range, e.g. `3-10`, `1,3,5`. Off-by-one: page
  ranges are inclusive of both ends.
- `model` — `default` or `pulse-ultra-2`.
- `figure_processing`, `spreadsheet`, `extensions`, `storage`, `async`,
  refine options for ultra-2.

## /extract response shape

Standard:
- `markdown` — primary output.
- `page_count`, `extraction_id`, `extraction_url`, `credits_used`,
  `plan_info`, `bounding_boxes`, `extensions`, `warnings`.

Large response (~70+ pages or >5MB): returns `{is_url: true, url: ...}`
with a single-use, 1-hour expiry signed URL. Auth the GET with the
same `x-api-key`.

## Limits (default model)

No published file-size or page-count cap; switches to URL-delivery at
~70 pages or 5MB. Rate limits not stated for default model.
Pulse-ultra-2: 5/min, 20/hr, 50MB, 2 concurrent.

## Errors observed

- `AUTH_001` "API key is required" — header missing or not parsed
  (HTTP 401).
- `REQ_001` "No file or URL provided" — auth OK, no document attached
  (HTTP 400).
- `REQ_006` "Range X-Y: end page exceeds doc length (N)" — `pages`
  parameter out of bounds (HTTP 400).

## Quality observations from the BCG ingest

Tested on the 9M FY26 BCG Banking Sector Roundup (48-page slide deck):
- **Visual dashboard pages with tile-style infographics (page 2)**:
  parser collapses the layout into HTML tables but cell-to-value
  alignment is unreliable (colspan/rowspan confusion, leaked currency
  glyphs, merged headers). For these, manual transcription from the
  rendered image is more accurate.
- **Prose summary pages (page 4-5)**: clean, with all bullets
  preserved, including secondary claims not present on the snapshot
  page (e.g., RBI cut repo by 125 bps since Feb 2025; CRR -100 bps
  added ~₹2.5 lakh crore; deposit rates stayed sticky in Q3 FY26).
- **Structured per-category tables (RoA tree, page 12-13)**: extracted
  cleanly. Bank-category-level breakdowns of NIM, fee income, opex,
  PPOP, credit costs, tax, ROA recovered exactly.
- **Charts (bar/line)**: numeric labels extracted as a flat list of
  numbers without their associated x-axis category, rendering them
  unreliable for citation.

Implication: aim Pulse at prose and structured tables (pages 3+ of
each deck), not at infographic-style summary pages, and not at
chart-only pages.
