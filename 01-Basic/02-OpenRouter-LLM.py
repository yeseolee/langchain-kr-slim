from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model, print_stream

llm = make_chat_model(temperature=0.1)

question = "대한민국의 수도는 어디인가요?"
response = llm.invoke(question)

print("[content]")
print(response.content)
print()

print("[response_metadata]")
print(response.response_metadata)
print()

print("[stream]")
stream = llm.stream("대한민국의 대표 관광지 5곳과 간단한 설명을 알려주세요.")
print_stream(stream)
