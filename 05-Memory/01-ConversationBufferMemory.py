from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.chat_history import InMemoryChatMessageHistory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

history = InMemoryChatMessageHistory()

turns = [
    (
        "안녕하세요, 비대면으로 은행 계좌를 개설하고 싶습니다. 어떻게 시작해야 하나요?",
        "먼저 본인 인증을 위해 신분증을 준비해 주세요.",
    ),
    (
        "네, 신분증을 준비했습니다. 이제 무엇을 해야 하나요?",
        "신분증 앞뒤를 촬영해 업로드해 주세요.",
    ),
    (
        "사진을 업로드했습니다. 본인 인증은 어떻게 진행되나요?",
        "휴대폰 본인 인증을 진행하고 문자 인증번호를 입력해 주세요.",
    ),
]

for user_text, ai_text in turns:
    history.add_user_message(user_text)
    history.add_ai_message(ai_text)

for message in history.messages:
    print(f"{message.type}: {message.content}")
