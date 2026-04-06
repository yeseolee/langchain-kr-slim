from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model


class Topic(BaseModel):
    description: str = Field(description="주제에 대한 간결한 설명")
    hashtags: str = Field(description="해시태그 형식의 키워드(2개 이상)")


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "질문에 간결하게 답변하세요."),
        ("user", "#Format: {format_instructions}\n\n#Question: {question}"),
    ]
)
llm = make_chat_model(temperature=0)

typed_parser = JsonOutputParser(pydantic_object=Topic)
typed_chain = (
    prompt.partial(format_instructions=typed_parser.get_format_instructions())
    | llm
    | typed_parser
)
typed_response = typed_chain.invoke({"question": "지구 온난화의 심각성을 알려주세요."})
print(typed_response)

freeform_parser = JsonOutputParser()
freeform_chain = (
    prompt.partial(format_instructions=freeform_parser.get_format_instructions())
    | llm
    | freeform_parser
)
freeform_response = freeform_chain.invoke(
    {
        "question": (
            "지구 온난화에 대해 알려주세요. 설명은 description, "
            "관련 키워드는 hashtags에 담아주세요."
        )
    }
)
print(freeform_response)
