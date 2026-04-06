from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model

llm = make_chat_model(temperature=0)
response = llm.invoke("대한민국의 수도는 어디인가요?")

print("[content]")
print(response.content)
print()

print("[token_usage]")
print(response.response_metadata.get("token_usage", {}))
print()

print("[full_response_metadata]")
print(response.response_metadata)
