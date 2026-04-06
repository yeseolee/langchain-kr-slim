from __future__ import annotations

import sys
from datetime import datetime
from operator import itemgetter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough

from langchain_cookbook.example_utils import make_chat_model

llm = make_chat_model(temperature=0.0)
prompt = PromptTemplate.from_template("{num}의 10배는?")
chain = prompt | llm

print("[invoke-dict]")
print(chain.invoke({"num": 5}))
print()

runnable_chain = {"num": RunnablePassthrough()} | prompt | llm
print("[passthrough]")
print(runnable_chain.invoke(10))
print()

assigned = RunnablePassthrough.assign(new_num=lambda x: x["num"] * 3)
print("[assign]")
print(assigned.invoke({"num": 1}))
print()

parallel = RunnableParallel(
    passed=RunnablePassthrough(),
    extra=RunnablePassthrough.assign(mult=lambda x: x["num"] * 3),
    modified=lambda x: x["num"] + 1,
)
print("[parallel]")
print(parallel.invoke({"num": 1}))
print()


def get_today(_: object) -> str:
    return datetime.today().strftime("%b-%d")


birthday_prompt = PromptTemplate.from_template(
    "{today}가 생일인 유명인 {n}명을 나열하세요. 생년월일도 적어주세요."
)
birthday_chain = (
    {"today": RunnableLambda(get_today), "n": RunnablePassthrough()}
    | birthday_prompt
    | llm
    | StrOutputParser()
)
print("[lambda]")
print(birthday_chain.invoke(3))
print()


def length_function(text: str) -> int:
    return len(text)


def multiple_length_function(values: dict[str, str]) -> int:
    return len(values["text1"]) * len(values["text2"])


math_prompt = ChatPromptTemplate.from_template("{a} + {b} 는 무엇인가요?")
math_chain = (
    {
        "a": itemgetter("word1") | RunnableLambda(length_function),
        "b": {"text1": itemgetter("word1"), "text2": itemgetter("word2")}
        | RunnableLambda(multiple_length_function),
    }
    | math_prompt
    | llm
    | StrOutputParser()
)

print("[itemgetter-lambda]")
print(math_chain.invoke({"word1": "hello", "word2": "world"}))
