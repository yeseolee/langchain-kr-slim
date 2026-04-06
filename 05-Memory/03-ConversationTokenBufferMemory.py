from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Message:
    role: str
    content: str


def count_tokens(text: str) -> int:
    try:
        from transformers import AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained("gpt2", local_files_only=True)
        return len(tokenizer.encode(text))
    except Exception:
        return max(1, len(text.split()))


def trim_messages(messages: list[Message], max_token_limit: int) -> list[Message]:
    trimmed = messages[:]
    while trimmed:
        token_total = sum(count_tokens(message.content) for message in trimmed)
        if token_total <= max_token_limit:
            return trimmed
        trimmed.pop(0)
    return trimmed


conversation = [
    Message(
        "human",
        "안녕하세요. 최근에 구매한 공작 기계 XG-200 설치 절차를 알고 싶습니다.",
    ),
    Message("ai", "먼저 220V 전원과 안전 접지가 가능한지 확인해 주세요."),
    Message("human", "전원은 준비됐습니다. 다음 단계는 무엇인가요?"),
    Message("ai", "기계를 평평한 바닥에 고정하고 케이블을 연결해 주세요."),
    Message("human", "초기 소프트웨어 설정도 필요한가요?"),
    Message("ai", "네. 제어 패널에서 언어와 단위를 설정한 뒤 자가 진단을 실행하세요."),
]

buffer = trim_messages(conversation, max_token_limit=180)
print("retained_messages")
for message in buffer:
    print(f"- {message.role}: {message.content}")
print("token_total", sum(count_tokens(message.content) for message in buffer))
