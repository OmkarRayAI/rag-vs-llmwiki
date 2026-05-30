"""RAG baseline: chunk the 6 BCG PDFs, embed locally, top-k, generate.

Index is built once and cached at eval/runs/_rag_index.npz. Re-run with
--rebuild to regenerate.

Embeddings: local sentence-transformers (all-MiniLM-L6-v2). No API key.
Chunking: per-page text from pypdf, 350-word windows with 50-word overlap.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _models import answer  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
RAW_DIR = REPO_ROOT / "raw"
INDEX_PATH = REPO_ROOT / "eval" / "runs" / "_rag_index.npz"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_WORDS = 350
OVERLAP = 50
TOP_K = 8

_model = None


def _embedder():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(EMBED_MODEL)
    return _model


@dataclass
class Chunk:
    text: str
    source: str
    page: int


def chunk_pdfs() -> list[Chunk]:
    from pypdf import PdfReader

    chunks: list[Chunk] = []
    pdfs = sorted(RAW_DIR.glob("banking-sector-roundup-*.pdf"))
    for pdf in pdfs:
        reader = PdfReader(str(pdf))
        for page_idx, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            words = text.split()
            if not words:
                continue
            i = 0
            while i < len(words):
                window = words[i : i + CHUNK_WORDS]
                chunks.append(
                    Chunk(text=" ".join(window), source=pdf.name, page=page_idx)
                )
                if i + CHUNK_WORDS >= len(words):
                    break
                i += CHUNK_WORDS - OVERLAP
    return chunks


def embed(texts: list[str]) -> np.ndarray:
    return np.asarray(_embedder().encode(texts, show_progress_bar=False), dtype=np.float32)


def build_index(force: bool = False) -> tuple[np.ndarray, list[Chunk]]:
    if INDEX_PATH.exists() and not force:
        data = np.load(INDEX_PATH, allow_pickle=True)
        return data["embeddings"], list(data["chunks"])
    print("Building RAG index (local embeddings)...", file=sys.stderr)
    chunks = chunk_pdfs()
    print(f"  chunks: {len(chunks)}", file=sys.stderr)
    embeddings = embed([c.text for c in chunks])
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        INDEX_PATH,
        embeddings=embeddings,
        chunks=np.array(chunks, dtype=object),
    )
    return embeddings, chunks


def retrieve(question: str, embeddings: np.ndarray, chunks: list[Chunk]) -> list[Chunk]:
    qv = embed([question])[0]
    qv = qv / (np.linalg.norm(qv) + 1e-9)
    norms = embeddings / (np.linalg.norm(embeddings, axis=1, keepdims=True) + 1e-9)
    sims = norms @ qv
    top = np.argsort(-sims)[:TOP_K]
    return [chunks[i] for i in top]


SYSTEM = """You are a research assistant answering questions from retrieved
document passages. The passages are excerpts from BCG Banking Sector Roundup
PDFs.

Your job:
1. Read the passages provided below.
2. Answer the user's question precisely.
3. Cite which passage each claim came from by source filename and page number,
   e.g. [banking-sector-roundup-9mfy26.pdf p.12].
4. If the passages don't contain enough information, say so explicitly.
5. Do NOT fabricate numbers. If a number isn't in the passages, say so.

PASSAGES BELOW.
==============
"""


def query(question: str, model_id: str) -> str:
    embeddings, chunks = build_index()
    hits = retrieve(question, embeddings, chunks)
    context = "\n\n".join(
        f"--- [{h.source} p.{h.page}] ---\n{h.text}" for h in hits
    )
    return answer(model_id, SYSTEM + context, question)


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "What was industry GNPA in 9M FY26?"
    model = sys.argv[2] if len(sys.argv) > 2 else "claude-sonnet-4-6"
    print(query(q, model))
