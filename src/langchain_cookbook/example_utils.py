from __future__ import annotations

from pathlib import Path
from typing import Iterable

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_cookbook.openrouter_setup import make_chat_model

DEFAULT_EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def project_root_from_script(script_path: str | Path) -> Path:
    return Path(script_path).resolve().parents[1]


def make_local_embeddings(
    model_name: str = DEFAULT_EMBEDDING_MODEL,
    *,
    device: str = "cuda",
    normalize_embeddings: bool = True,
    batch_size: int = 16,
) -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": device},
        encode_kwargs={
            "normalize_embeddings": normalize_embeddings,
            "batch_size": batch_size,
        },
    )


def print_stream(chunks: Iterable[object]) -> None:
    for chunk in chunks:
        content = getattr(chunk, "content", "")
        if not content:
            continue
        print(content, end="", flush=True)
    print()


__all__ = [
    "DEFAULT_EMBEDDING_MODEL",
    "make_chat_model",
    "make_local_embeddings",
    "print_stream",
    "project_root_from_script",
]
