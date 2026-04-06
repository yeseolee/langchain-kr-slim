from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.embedding_utils import cosine_similarity
from langchain_cookbook.example_utils import make_local_embeddings

texts = [
    "안녕, 만나서 반가워.",
    "LangChain simplifies the process of building applications with large language models.",
    "랭체인 한국어 튜토리얼은 LangChain을 더 쉽게 활용할 수 있도록 구성되어 있습니다.",
    "LangChain은 초거대 언어모델로 애플리케이션을 구축하는 과정을 단순화합니다.",
    "Retrieval-Augmented Generation (RAG) is an effective technique for improving AI responses.",
]

embeddings = make_local_embeddings()
embedded_documents = embeddings.embed_documents(texts)
embedded_query = embeddings.embed_query("LangChain 에 대해서 알려주세요.")

print(f"dimension={len(embedded_documents[0])}")

ranked = sorted(
    (
        (cosine_similarity(embedded_query, vector), text)
        for text, vector in zip(texts, embedded_documents, strict=True)
    ),
    reverse=True,
)

print("[Query] LangChain 에 대해서 알려주세요.")
for score, text in ranked:
    print(f"[{score:.4f}] {text}")
