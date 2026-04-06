from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model


def unstable_runnable(_: dict) -> str:
    raise RuntimeError("simulated temporary failure")


prompt = PromptTemplate.from_template("{topic}을 두 문장으로 요약하세요.")
fallback_chain = prompt | make_chat_model(temperature=0)
chain = RunnableLambda(unstable_runnable).with_fallbacks([fallback_chain])

result = chain.invoke({"topic": "LangChain expression language"})
print(result.content if hasattr(result, "content") else result)
