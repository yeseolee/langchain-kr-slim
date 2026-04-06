from __future__ import annotations

import sys
from enum import Enum
from pathlib import Path

from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import PromptTemplate

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model


class Colors(Enum):
    RED = "빨간색"
    GREEN = "초록색"
    BLUE = "파란색"


class ColorOutputParser(BaseOutputParser[Colors]):
    def get_format_instructions(self) -> str:
        options = ", ".join(color.value for color in Colors)
        return f"다음 값 중 하나만 답하세요: {options}"

    def parse(self, text: str) -> Colors:
        normalized = text.strip().splitlines()[0].strip("`\"' ")
        for color in Colors:
            if normalized == color.value:
                return color
        raise ValueError(f"지원하지 않는 색상입니다: {text!r}")


parser = ColorOutputParser()
prompt = PromptTemplate.from_template(
    """
다음 물체의 색상을 판단하세요.

Object: {object}
Instructions: {instructions}
"""
).partial(instructions=parser.get_format_instructions())

chain = prompt | make_chat_model(temperature=0) | parser
response = chain.invoke({"object": "하늘"})

print(response)
print(response.value)
