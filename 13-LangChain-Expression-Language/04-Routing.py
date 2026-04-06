from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model

llm = make_chat_model(temperature=0)

poem_chain = (
    PromptTemplate.from_template("{question}에 대해 두 줄짜리 시를 써주세요.")
    | llm
    | StrOutputParser()
)
qa_chain = (
    PromptTemplate.from_template("{question}에 대해 간결하게 설명하세요.")
    | llm
    | StrOutputParser()
)


def route(info: dict[str, str]):
    if "시" in info["question"]:
        return poem_chain.invoke(info)
    return qa_chain.invoke(info)


chain = RunnableLambda(route)
print(chain.invoke({"question": "LCEL 이 무엇인지 설명해줘"}))
print(chain.invoke({"question": "바다에 대한 짧은 시를 써줘"}))
