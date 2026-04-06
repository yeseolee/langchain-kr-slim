from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import chain

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model


@chain
def explain_topic(topic: str) -> str:
    runnable = (
        PromptTemplate.from_template("{topic} 를 초보자 기준으로 두 문장으로 설명하세요.")
        | make_chat_model(temperature=0)
        | StrOutputParser()
    )
    return runnable.invoke({"topic": topic})


print(explain_topic.invoke("RunnableParallel"))
