from __future__ import annotations

import json
import sys
from pathlib import Path

from langchain_core.documents import Document
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore
from pydantic import BaseModel, Field

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model, make_local_embeddings


class StructuredQuery(BaseModel):
    semantic_query: str = Field(description="임베딩 검색에 사용할 문장")
    category: str | None = None
    year_gte: int | None = None
    min_rating: float | None = None


docs = [
    Document(
        page_content="히알루론산 세럼으로 깊은 보습을 제공합니다.",
        metadata={"year": 2024, "category": "스킨케어", "rating": 4.7},
    ),
    Document(
        page_content="매트 피니시 파운데이션으로 모공을 자연스럽게 커버합니다.",
        metadata={"year": 2023, "category": "메이크업", "rating": 4.5},
    ),
    Document(
        page_content="식물성 성분 클렌징 오일로 메이크업을 부드럽게 지웁니다.",
        metadata={"year": 2023, "category": "클렌징", "rating": 4.8},
    ),
    Document(
        page_content="비타민 C 크림으로 피부 톤을 밝게 정리합니다.",
        metadata={"year": 2024, "category": "스킨케어", "rating": 4.6},
    ),
]

parser = PydanticOutputParser(pydantic_object=StructuredQuery)
prompt = PromptTemplate.from_template(
    """
사용자 질문을 semantic query 와 metadata filter 로 분해하세요.

허용된 category: 스킨케어, 메이크업, 클렌징

질문:
{question}

형식:
{format_instructions}
"""
).partial(format_instructions=parser.get_format_instructions())

question = "2024년 이후 출시된 평점 4.6 이상 스킨케어 제품을 찾아줘."
query_plan = (prompt | make_chat_model(temperature=0) | parser).invoke(
    {"question": question}
)

filtered_docs = [
    document
    for document in docs
    if (query_plan.category is None or document.metadata["category"] == query_plan.category)
    and (query_plan.year_gte is None or document.metadata["year"] >= query_plan.year_gte)
    and (
        query_plan.min_rating is None
        or document.metadata["rating"] >= query_plan.min_rating
    )
]

print(json.dumps(query_plan.model_dump(), ensure_ascii=False, indent=2))
if not filtered_docs:
    print("조건을 만족하는 문서가 없습니다.")
else:
    filtered_store = InMemoryVectorStore.from_documents(
        filtered_docs,
        embedding=make_local_embeddings(),
    )
    for document in filtered_store.similarity_search(query_plan.semantic_query, k=2):
        print(document.metadata)
        print(document.page_content)
        print("-" * 30)
