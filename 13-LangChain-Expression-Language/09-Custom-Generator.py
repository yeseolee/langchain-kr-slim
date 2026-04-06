from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterator

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableGenerator

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model


def split_comma_items(chunks: Iterator[str]) -> Iterator[str]:
    buffer = ""
    for chunk in chunks:
        buffer += chunk
        while "," in buffer:
            item, buffer = buffer.split(",", 1)
            cleaned = item.strip()
            if cleaned:
                yield cleaned
    cleaned = buffer.strip()
    if cleaned:
        yield cleaned


prompt = PromptTemplate.from_template(
    "{topic} 주제의 핵심 키워드 5개를 쉼표로만 구분해서 출력하세요."
)
chain = (
    prompt
    | make_chat_model(temperature=0)
    | StrOutputParser()
    | RunnableGenerator(split_comma_items)
)

for keyword in chain.stream({"topic": "LangChain RAG"}):
    print(keyword)
