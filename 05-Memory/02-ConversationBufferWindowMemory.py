from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.chat_history import InMemoryChatMessageHistory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.history_utils import last_k_turn_messages

history = InMemoryChatMessageHistory()

turns = [
    ("계좌를 개설하고 싶어요.", "먼저 신분증을 준비해 주세요."),
    ("신분증을 준비했어요.", "신분증 사진을 업로드해 주세요."),
    ("사진을 업로드했어요.", "이제 휴대폰 인증을 진행해 주세요."),
    ("인증번호를 입력했어요.", "마지막으로 계좌 정보를 확인해 주세요."),
    ("모든 절차를 완료했어요.", "계좌 개설이 완료되었습니다."),
]

for user_text, ai_text in turns:
    history.add_user_message(user_text)
    history.add_ai_message(ai_text)

window = last_k_turn_messages(history.messages, k=2)
for message in window:
    print(f"{message.type}: {message.content}")
