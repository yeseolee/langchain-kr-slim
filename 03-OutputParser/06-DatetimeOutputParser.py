from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path

from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import PromptTemplate

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model


class DateOnlyOutputParser(BaseOutputParser[datetime]):
    format = "%Y-%m-%d"

    def get_format_instructions(self) -> str:
        return "반드시 YYYY-MM-DD 형식의 날짜만 출력하세요."

    def parse(self, text: str) -> datetime:
        match = re.search(r"\d{4}-\d{2}-\d{2}", text)
        if match is None:
            raise ValueError(f"날짜를 찾지 못했습니다: {text!r}")
        return datetime.strptime(match.group(0), self.format)


parser = DateOnlyOutputParser()
prompt = PromptTemplate.from_template(
    """
질문에 답하세요.

형식:
{format_instructions}

질문:
{question}
"""
).partial(format_instructions=parser.get_format_instructions())

chain = prompt | make_chat_model(temperature=0) | parser
response = chain.invoke({"question": "Google 이 창업한 연도"})

print(response.strftime("%Y-%m-%d"))
