from __future__ import annotations

import json
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


class EntityFact(BaseModel):
    entity: str = Field(description="사람, 회사, 제품, 장소")
    fact: str = Field(description="entity 에 대한 짧은 사실")


class EntityFactList(BaseModel):
    items: list[EntityFact]


turns = [
    ("저는 김서연이고 판교에 있는 데이터팀에서 일합니다.", "확인했습니다."),
    ("우리 팀은 다음 달에 서울 코엑스에서 생성형 AI 세미나를 엽니다.", "행사 준비를 도와드릴게요."),
    ("발표 주제는 사내 검색 시스템 개선입니다.", "발표 주제를 기억해 두겠습니다."),
]

entity_store: dict[str, list[str]] = {}
parser = PydanticOutputParser(pydantic_object=EntityFactList)
prompt = PromptTemplate.from_template(
    """
대화에서 중요한 엔티티와 사실만 추출하세요.

대화:
{dialogue}

형식:
{format_instructions}
"""
).partial(format_instructions=parser.get_format_instructions())

chain = prompt | make_chat_model(temperature=0) | parser

history_lines: list[str] = []
for human_text, ai_text in turns:
    history_lines.append(f"human: {human_text}")
    history_lines.append(f"ai: {ai_text}")
    parsed = chain.invoke({"dialogue": "\n".join(history_lines)})
    for item in parsed.items:
        facts = entity_store.setdefault(item.entity, [])
        if item.fact not in facts:
            facts.append(item.fact)

print(json.dumps(entity_store, ensure_ascii=False, indent=2))
