from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model


data_dir = Path(__file__).resolve().parent / "data"
support_text = (data_dir / "의대증원찬성.txt").read_text(encoding="utf-8")
oppose_text = (data_dir / "의대증원반대.txt").read_text(encoding="utf-8")


def run_agent(name: str, stance: str, evidence: str, history: str) -> str:
    prompt = ChatPromptTemplate.from_template(
        """
당신은 {name} 입니다.
입장: {stance}

근거 문서:
{evidence}

이전 토론:
{history}

상대 주장에 반박하면서 자신의 입장을 3문장 이내로 제시하세요.
"""
    )
    chain = prompt | make_chat_model(temperature=0)
    return chain.invoke(
        {
            "name": name,
            "stance": stance,
            "evidence": evidence[:2000],
            "history": history or "토론 시작",
        }
    ).content


history = ""
for round_index in range(1, 3):
    support_message = run_agent("찬성 측", "의대 정원 확대 찬성", support_text, history)
    history += f"[찬성 측 {round_index}] {support_message}\n"
    oppose_message = run_agent("반대 측", "의대 정원 확대 반대", oppose_text, history)
    history += f"[반대 측 {round_index}] {oppose_message}\n"

print(history)
