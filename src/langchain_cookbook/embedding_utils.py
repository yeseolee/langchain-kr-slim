from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from langchain_core.embeddings import Embeddings


def cosine_similarity(left: list[float], right: list[float]) -> float:
    numerator = sum(a * b for a, b in zip(left, right, strict=True))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    return numerator / (left_norm * right_norm)


class DiskCachedEmbeddings(Embeddings):
    def __init__(
        self,
        *,
        underlying_embeddings: Embeddings,
        cache_path: str | Path,
        namespace: str,
    ) -> None:
        self.underlying_embeddings = underlying_embeddings
        self.cache_path = Path(cache_path)
        self.namespace = namespace
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.cache_path.exists():
            self.cache_path.write_text("{}", encoding="utf-8")

    def _load_cache(self) -> dict[str, list[float]]:
        return json.loads(self.cache_path.read_text(encoding="utf-8"))

    def _save_cache(self, cache: dict[str, list[float]]) -> None:
        self.cache_path.write_text(json.dumps(cache), encoding="utf-8")

    def _key(self, text: str) -> str:
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        return f"{self.namespace}:{digest}"

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        cache = self._load_cache()
        missing_texts = [text for text in texts if self._key(text) not in cache]

        if missing_texts:
            missing_vectors = self.underlying_embeddings.embed_documents(missing_texts)
            for text, vector in zip(missing_texts, missing_vectors, strict=True):
                cache[self._key(text)] = vector
            self._save_cache(cache)

        return [cache[self._key(text)] for text in texts]

    def embed_query(self, text: str) -> list[float]:
        cache = self._load_cache()
        key = self._key(text)
        if key not in cache:
            cache[key] = self.underlying_embeddings.embed_query(text)
            self._save_cache(cache)
        return cache[key]


__all__ = ["DiskCachedEmbeddings", "cosine_similarity"]
