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


class Triple(BaseModel):
    subject: str
    relation: str
    object: str


class TripleList(BaseModel):
    triples: list[Triple] = Field(default_factory=list)


dialogue = [
    "김셜리는 판교에 거주한다.",
    "김셜리는 우리 회사의 신입 디자이너다.",
    "신입 디자이너 팀장은 박민수다.",
]

parser = PydanticOutputParser(pydantic_object=TripleList)
prompt = PromptTemplate.from_template(
    """
문장에서 지식 그래프 삼중항만 추출하세요.

문장:
{text}

형식:
{format_instructions}
"""
).partial(format_instructions=parser.get_format_instructions())

chain = prompt | make_chat_model(temperature=0) | parser
graph: set[tuple[str, str, str]] = set()

for sentence in dialogue:
    triples = chain.invoke({"text": sentence})
    for triple in triples.triples:
        graph.add((triple.subject, triple.relation, triple.object))

print(json.dumps(sorted(graph), ensure_ascii=False, indent=2))
