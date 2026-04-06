from __future__ import annotations

import sys
from pathlib import Path

from kiwipiepy import Kiwi
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


kiwi = Kiwi()


def tokenize(text: str) -> list[str]:
    return [token.form for token in kiwi.tokenize(text) if token.form.strip()]


documents = [
    Document(page_content="Word2Vec은 단어를 밀집 벡터로 변환하는 분산 표현 기법입니다."),
    Document(page_content="BM25는 질의어와 문서의 통계적 일치를 기반으로 문서를 점수화합니다."),
    Document(page_content="임베딩 검색은 의미 유사도를 활용해 키워드가 달라도 관련 문서를 찾습니다."),
]

corpus = [tokenize(document.page_content) for document in documents]
bm25 = BM25Okapi(corpus)
query = "단어 임베딩 기법 설명"
scores = bm25.get_scores(tokenize(query))

for score, document in sorted(
    zip(scores, documents, strict=True),
    key=lambda item: item[0],
    reverse=True,
):
    print(round(float(score), 4), document.page_content)
