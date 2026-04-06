from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_local_embeddings


turns = [
    (
        "안녕하세요, 저는 컴퓨터 공학을 전공한 신입 개발자입니다.",
        "반갑습니다. 주로 다룬 기술 스택은 무엇인가요?",
    ),
    (
        "최근 프로젝트에서 FastAPI와 PostgreSQL을 사용했습니다.",
        "백엔드 경험이 있군요. 데이터베이스 설계도 해보셨나요?",
    ),
    (
        "네, 사용자와 주문 테이블을 설계하고 API를 연결했습니다.",
        "좋습니다. 협업 방식도 설명해 주세요.",
    ),
]

store = InMemoryVectorStore(embedding=make_local_embeddings())
documents: list[Document] = []
for turn_index, (human_text, ai_text) in enumerate(turns, start=1):
    documents.append(
        Document(
            page_content=f"human: {human_text}\nai: {ai_text}",
            metadata={"turn": turn_index},
        )
    )

store.add_documents(documents)
results = store.similarity_search("지원자는 어떤 데이터베이스를 사용했나요?", k=2)
for document in results:
    print(document.metadata)
    print(document.page_content)
    print("=" * 30)
