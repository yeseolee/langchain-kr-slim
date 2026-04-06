from __future__ import annotations

import re
import statistics

from langchain_cookbook.embedding_utils import cosine_similarity


def split_sentences(text: str) -> list[str]:
    raw_sentences = re.split(r"(?<=[.!?])\s+|\n+", text.strip())
    return [sentence.strip() for sentence in raw_sentences if sentence.strip()]


def semantic_chunk_text(
    text: str,
    *,
    embeddings,
    context_window: int = 1,
    max_sentences_per_chunk: int = 4,
) -> list[str]:
    sentences = split_sentences(text)
    if len(sentences) <= 1:
        return sentences

    windows: list[str] = []
    for index in range(len(sentences)):
        start = max(0, index - context_window)
        end = min(len(sentences), index + context_window + 1)
        windows.append(" ".join(sentences[start:end]))

    vectors = embeddings.embed_documents(windows)
    similarities = [
        cosine_similarity(vectors[index], vectors[index + 1])
        for index in range(len(vectors) - 1)
    ]

    if len(similarities) > 1:
        mean_similarity = statistics.mean(similarities)
        std_similarity = statistics.pstdev(similarities)
        threshold = mean_similarity - std_similarity * 0.5
    else:
        threshold = similarities[0]

    chunks: list[str] = []
    current_chunk = [sentences[0]]

    for index, similarity in enumerate(similarities, start=1):
        boundary = similarity < threshold
        too_long = len(current_chunk) >= max_sentences_per_chunk
        if boundary or too_long:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentences[index]]
        else:
            current_chunk.append(sentences[index])

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


__all__ = ["semantic_chunk_text", "split_sentences"]
