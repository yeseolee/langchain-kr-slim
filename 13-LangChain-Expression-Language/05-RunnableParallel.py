from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model

llm = make_chat_model(temperature=0)
summary_chain = (
    PromptTemplate.from_template("{topic} 를 한 문장으로 요약하세요.")
    | llm
    | StrOutputParser()
)
keywords_chain = (
    PromptTemplate.from_template("{topic} 의 핵심 키워드 3개를 쉼표로 나열하세요.")
    | llm
    | StrOutputParser()
)

parallel = RunnableParallel(summary=summary_chain, keywords=keywords_chain)
print(parallel.invoke({"topic": "RAG"}))
