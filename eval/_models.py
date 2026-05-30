"""Thin model wrapper. Single provider (OpenRouter) gives us both vendors.

answer(model_id, system, user) -> str
"""

from __future__ import annotations

import json
import os
import time
from http.client import IncompleteRead, RemoteDisconnected
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

OPENROUTER = "https://openrouter.ai/api/v1/chat/completions"

# Local id -> OpenRouter model slug
MODELS = {
    "claude-sonnet-4-6": "anthropic/claude-sonnet-4.6",
    "gpt-5-mini": "openai/gpt-5-mini",
}


def answer(model_id: str, system: str, user: str) -> str:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not set (see .env.example)")
    if model_id not in MODELS:
        raise ValueError(f"Unknown model: {model_id}. Known: {list(MODELS)}")

    body = json.dumps({
        "model": MODELS[model_id],
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "max_tokens": 2000,
    }).encode()

    req = Request(
        OPENROUTER,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/local/llm-wiki",
            "X-Title": "llm-wiki eval",
        },
    )
    last_err: Exception | None = None
    for attempt in range(4):
        try:
            with urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read().decode())
            break
        except HTTPError as e:
            body = e.read().decode()[:500]
            if e.code in (429, 500, 502, 503, 504):
                last_err = RuntimeError(f"OpenRouter {e.code}: {body}")
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"OpenRouter {e.code}: {body}") from e
        except (IncompleteRead, RemoteDisconnected, URLError, TimeoutError) as e:
            last_err = e
            time.sleep(2 ** attempt)
            continue
    else:
        raise RuntimeError(f"OpenRouter failed after 4 attempts: {last_err}")

    return data["choices"][0]["message"]["content"] or ""
