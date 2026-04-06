from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model, print_stream

llm = make_chat_model(temperature=0)

response = llm.invoke("사랑이 무엇인지 3문장으로 설명하세요.")
print("[invoke]")
print(response.content)
print()

print("[response_metadata]")
print(response.response_metadata)
print()

print("[stream]")
print_stream(llm.stream("파이썬으로 로또 번호 6개를 생성하는 함수를 작성하세요."))
