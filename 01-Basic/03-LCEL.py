from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from langchain_cookbook.example_utils import make_chat_model, print_stream

prompt = PromptTemplate.from_template("{country}의 수도는 어디인가요?")
llm = make_chat_model(temperature=0.0)
chain = prompt | llm | StrOutputParser()

print("[invoke]")
print(chain.invoke({"country": "대한민국"}))
print()

print("[stream]")
print_stream(chain.stream({"country": "일본"}))
