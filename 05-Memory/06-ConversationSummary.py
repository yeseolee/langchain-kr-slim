from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.prompts import PromptTemplate

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model


turns = [
    ("유럽 여행 패키지 가격이 얼마인가요?", "기본 상품은 3,500유로이며 항공과 호텔이 포함됩니다."),
    ("주요 관광지는 어디인가요?", "파리, 로마, 베를린, 취리히 대표 명소를 방문합니다."),
    ("보험도 포함되나요?", "기본 여행자 보험이 포함되고 상향 옵션도 가능합니다."),
]

summary_prompt = PromptTemplate.from_template(
    """
이전 요약:
{summary}

새 대화:
human: {human}
ai: {ai}

이전 요약을 유지하면서 새 정보만 반영한 최신 요약을 3문장 이내로 작성하세요.
"""
)

chain = summary_prompt | make_chat_model(temperature=0)
summary = "아직 요약 없음."

for human_text, ai_text in turns:
    summary = chain.invoke(
        {"summary": summary, "human": human_text, "ai": ai_text}
    ).content

print(summary)
