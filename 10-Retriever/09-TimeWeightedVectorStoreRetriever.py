from __future__ import annotations

import math
import sys
from datetime import datetime, timedelta
from pathlib import Path

from langchain_core.documents import Document

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.embedding_utils import cosine_similarity
from langchain_cookbook.example_utils import make_local_embeddings


now = datetime.now()
documents = [
    Document(
        page_content="지난주 회의에서 검색 품질 개선을 위해 BM25 와 벡터 검색을 함께 쓰기로 했다.",
        metadata={"saved_at": (now - timedelta(days=7)).isoformat()},
    ),
    Document(
        page_content="오늘 회의에서는 검색 결과 재정렬을 위해 reranker 를 붙이기로 결정했다.",
        metadata={"saved_at": now.isoformat()},
    ),
    Document(
        page_content="어제 메모: 임베딩 캐시 디렉터리를 팀 공용 경로로 옮겼다.",
        metadata={"saved_at": (now - timedelta(days=1)).isoformat()},
    ),
]

embeddings = make_local_embeddings()
query = "최근 검색 품질 개선 논의"
query_vector = embeddings.embed_query(query)
doc_vectors = embeddings.embed_documents([document.page_content for document in documents])

scored: list[tuple[float, Document]] = []
for document, vector in zip(documents, doc_vectors, strict=True):
    age_hours = (
        now - datetime.fromisoformat(document.metadata["saved_at"])
    ).total_seconds() / 3600
    freshness = math.exp(-0.03 * age_hours)
    similarity = cosine_similarity(query_vector, vector)
    score = similarity * 0.7 + freshness * 0.3
    scored.append((score, document))

for score, document in sorted(scored, key=lambda item: item[0], reverse=True):
    print(round(score, 4), document.metadata["saved_at"])
    print(document.page_content)
    print("-" * 30)
