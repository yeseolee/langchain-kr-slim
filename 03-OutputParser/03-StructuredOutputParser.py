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


class AnswerWithSource(BaseModel):
    answer: str = Field(description="질문에 대한 답변")
    source: str = Field(description="답변의 출처 또는 근거")


parser = PydanticOutputParser(pydantic_object=AnswerWithSource)
prompt = PromptTemplate(
    template=(
        "answer the users question as best as possible.\n"
        "{format_instructions}\n"
        "{question}"
    ),
    input_variables=["question"],
    partial_variables={
        "format_instructions": parser.get_format_instructions(),
    },
)

chain = prompt | make_chat_model(temperature=0) | parser
response = chain.invoke({"question": "세종대왕의 업적은 무엇인가요?"})

print(response.model_dump_json(indent=2, ensure_ascii=False))
