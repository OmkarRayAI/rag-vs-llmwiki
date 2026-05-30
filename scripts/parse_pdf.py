"""Send a PDF to Pulse /extract and write the returned markdown.

Usage:
    python scripts/parse_pdf.py raw/banking-sector-roundup-9mfy26.pdf
    python scripts/parse_pdf.py raw/some.pdf --pages 3-10 --out raw/some.parsed.md

Env: PULSE_API_KEY must be set (loaded from .env if python-dotenv is installed,
otherwise from the shell environment).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError

PULSE_EXTRACT = "https://api.runpulse.com/extract"


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())


def multipart_body(pdf_path: Path, fields: dict[str, str]) -> tuple[bytes, str]:
    boundary = "----pulse" + str(int(time.time() * 1000))
    crlf = b"\r\n"
    body = b""
    for k, v in fields.items():
        body += f"--{boundary}{chr(13)}{chr(10)}".encode()
        body += f'Content-Disposition: form-data; name="{k}"{chr(13)}{chr(10)}{chr(13)}{chr(10)}{v}{chr(13)}{chr(10)}'.encode()
    body += f"--{boundary}{chr(13)}{chr(10)}".encode()
    body += f'Content-Disposition: form-data; name="file"; filename="{pdf_path.name}"{chr(13)}{chr(10)}'.encode()
    body += b"Content-Type: application/pdf" + crlf + crlf
    body += pdf_path.read_bytes()
    body += crlf + f"--{boundary}--{chr(13)}{chr(10)}".encode()
    return body, boundary


def call_pulse(pdf_path: Path, pages: str | None) -> dict:
    api_key = os.environ.get("PULSE_API_KEY")
    if not api_key:
        sys.exit("PULSE_API_KEY not set. See .env.example.")
    fields = {}
    if pages:
        fields["pages"] = pages
    body, boundary = multipart_body(pdf_path, fields)
    req = Request(
        PULSE_EXTRACT,
        data=body,
        method="POST",
        headers={
            "x-api-key": api_key,
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
    )
    try:
        with urlopen(req, timeout=300) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        sys.exit(f"Pulse error {e.code}: {e.read().decode()[:500]}")


def fetch_large_result(url: str) -> dict:
    api_key = os.environ.get("PULSE_API_KEY", "")
    req = Request(url, headers={"x-api-key": api_key})
    with urlopen(req, timeout=300) as resp:
        return json.loads(resp.read().decode())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--pages", help="1-indexed range, e.g. '3-10' or '1,3,5'")
    ap.add_argument("--out", help="Output markdown path (default: <pdf>.parsed.md)")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    load_env_file(repo_root / ".env")

    pdf_path = Path(args.pdf).resolve()
    if not pdf_path.exists():
        sys.exit(f"Not found: {pdf_path}")

    out_path = Path(args.out) if args.out else pdf_path.with_suffix(".parsed.md")

    print(f"Parsing {pdf_path.name} (pages={args.pages or 'all'})...", file=sys.stderr)
    result = call_pulse(pdf_path, args.pages)

    if result.get("is_url"):
        print("Large response; fetching from signed URL...", file=sys.stderr)
        result = fetch_large_result(result["url"])

    md = result.get("markdown")
    if not md:
        sys.exit(f"No markdown in response. Keys: {list(result)}")

    page_count = result.get("page_count")
    credits = result.get("credits_used")
    out_path.write_text(md)
    print(
        f"Wrote {out_path} ({len(md)} chars, page_count={page_count}, credits={credits})",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
