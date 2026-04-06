from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_cookbook.example_utils import make_chat_model

llm = make_chat_model()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant"),
        ("user", "{country}의 수도는 어디인가요?"),
    ]
)

print("[basic-chat-prompt]")
print((prompt | llm | StrOutputParser()).invoke({"country": "대한민국"}))
print()

message_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "당신은 친절한 AI 어시스턴트입니다. 이름은 {name} 입니다."),
        ("human", "반가워요!"),
        ("ai", "안녕하세요! 무엇을 도와드릴까요?"),
        ("human", "{user_input}"),
    ]
)
print("[messages]")
print(
    (message_prompt | llm | StrOutputParser()).invoke(
        {"name": "Teddy", "user_input": "당신의 이름은 무엇입니까?"}
    )
)
print()

summary_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "주요 키워드 중심으로 대화를 요약하세요."),
        MessagesPlaceholder(variable_name="conversation"),
        ("human", "지금까지의 대화를 {word_count} 단어로 요약하세요."),
    ]
)

summary_chain = summary_prompt | llm | StrOutputParser()
print("[messages-placeholder]")
print(
    summary_chain.invoke(
        {
            "word_count": 8,
            "conversation": [
                ("human", "안녕하세요! 저는 오늘 새로 입사한 테디입니다."),
                ("ai", "반갑습니다. 앞으로 잘 부탁드립니다."),
                ("human", "회사의 주요 제품군을 먼저 알고 싶습니다."),
                ("ai", "데이터 분석 플랫폼과 자동화 솔루션이 핵심입니다."),
            ],
        }
    )
)
