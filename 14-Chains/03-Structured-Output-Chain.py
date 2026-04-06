from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model


class CompanySummary(BaseModel):
    company: str = Field(description="회사 이름")
    product: str = Field(description="핵심 제품 또는 서비스")
    strength: str = Field(description="핵심 강점")


parser = PydanticOutputParser(pydantic_object=CompanySummary)
prompt = PromptTemplate.from_template(
    """
다음 설명을 구조화하세요.

설명:
{text}

형식:
{format_instructions}
"""
).partial(format_instructions=parser.get_format_instructions())

chain = prompt | make_chat_model(temperature=0) | parser
result = chain.invoke(
    {
        "text": (
            "테디소프트는 한국어 AI 실습 자료를 제공하는 교육 회사이며, "
            "핵심 강점은 초보자 친화적인 실습 예제를 빠르게 제공하는 점입니다."
        )
    }
)

print(result.model_dump_json(indent=2, ensure_ascii=False))
