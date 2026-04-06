from __future__ import annotations

import asyncio
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel

from langchain_cookbook.example_utils import make_chat_model

llm = make_chat_model()
chain = (
    PromptTemplate.from_template("{topic}를 3문장으로 설명하세요.")
    | llm
    | StrOutputParser()
)

print("[invoke]")
print(chain.invoke({"topic": "멀티모달"}))
print()

print("[batch]")
print(
    chain.batch(
        [
            {"topic": "ChatGPT"},
            {"topic": "Instagram"},
            {"topic": "프로그래밍"},
        ],
        config={"max_concurrency": 3},
    )
)
print()

capital_chain = (
    PromptTemplate.from_template("{country}의 수도는 어디야?")
    | llm
    | StrOutputParser()
)
area_chain = (
    PromptTemplate.from_template("{country}의 면적은 얼마야?")
    | llm
    | StrOutputParser()
)
combined = RunnableParallel(capital=capital_chain, area=area_chain)

print("[parallel]")
print(combined.invoke({"country": "대한민국"}))
print()


async def main() -> None:
    print("[ainvoke]")
    print(await chain.ainvoke({"topic": "비동기 실행"}))
    print()

    print("[abatch]")
    print(
        await chain.abatch(
            [
                {"topic": "YouTube"},
                {"topic": "Facebook"},
            ]
        )
    )


asyncio.run(main())
