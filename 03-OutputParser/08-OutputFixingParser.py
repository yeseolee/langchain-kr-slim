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


class Actor(BaseModel):
    name: str = Field(description="배우 이름")
    film_names: list[str] = Field(description="출연 영화 제목 목록")


parser = PydanticOutputParser(pydantic_object=Actor)
misformatted = "{'name': 'Tom Hanks', 'film_names': ['Forrest Gump']}"

try:
    parser.parse(misformatted)
except Exception as exc:
    print(f"[parse_error] {exc}")

repair_prompt = PromptTemplate.from_template(
    """
다음 문자열을 지정된 형식의 올바른 JSON으로 고치세요.

형식:
{format_instructions}

원본 문자열:
{raw_text}
"""
).partial(format_instructions=parser.get_format_instructions())

repair_chain = repair_prompt | make_chat_model(temperature=0) | parser
actor = repair_chain.invoke({"raw_text": misformatted})

print(actor.model_dump_json(indent=2, ensure_ascii=False))
