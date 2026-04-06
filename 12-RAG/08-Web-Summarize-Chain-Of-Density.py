from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model

source_path = Path(__file__).resolve().parent / "data" / "chain-of-density.txt"
source_text = source_path.read_text(encoding="utf-8")

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "주어진 글을 더 조밀하게 요약하세요. 이전 요약보다 정보 밀도는 높이고 길이는 비슷하게 유지하세요.",
        ),
        (
            "human",
            "원문:\n{source_text}\n\n이전 요약:\n{previous_summary}\n\n새 요약을 작성하세요.",
        ),
    ]
)
chain = prompt | make_chat_model(temperature=0) | StrOutputParser()

summary = "핵심 내용을 짧게 요약하세요."
for step in range(1, 4):
    summary = chain.invoke({"source_text": source_text, "previous_summary": summary})
    print(f"[step {step}]")
    print(summary)
    print("=" * 30)
