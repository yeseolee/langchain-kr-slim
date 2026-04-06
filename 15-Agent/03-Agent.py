from __future__ import annotations

import sys
from pathlib import Path

from langchain.agents import create_agent
from langchain.tools import tool

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model


@tool
def add_numbers(a: float, b: float) -> float:
    """Add two floating point numbers."""
    return a + b


@tool
def search_local_notes(query: str) -> str:
    """Search the local appendix note and return matching lines."""
    data_path = Path(__file__).resolve().parent / "data" / "appendix-keywords.txt"
    lines = data_path.read_text(encoding="utf-8").splitlines()
    matches = [line for line in lines if query.lower() in line.lower()]
    return "\n".join(matches[:5]) or "검색 결과가 없습니다."


agent = create_agent(
    model=make_chat_model(temperature=0),
    tools=[add_numbers, search_local_notes],
    system_prompt=(
        "You are a helpful assistant. "
        "Use the search_local_notes tool when the user asks about local documents."
    ),
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "appendix 문서에서 Word2Vec 관련 내용을 찾고 100과 24를 더한 값도 함께 알려줘.",
            }
        ]
    }
)
print(result["messages"][-1].content)
