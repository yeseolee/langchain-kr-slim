from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate, load_prompt

from langchain_cookbook.example_utils import make_chat_model

llm = make_chat_model()

prompt = PromptTemplate.from_template("{country}의 수도는 어디인가요?")
print("[format]")
print(prompt.format(country="대한민국"))
print()

chain = prompt | llm | StrOutputParser()
print("[invoke]")
print(chain.invoke({"country": "대한민국"}))
print()

partial_prompt = PromptTemplate(
    template="{country1}과 {country2}의 수도는 각각 어디인가요?",
    input_variables=["country1"],
    partial_variables={"country2": "미국"},
)
print("[partial]")
print(partial_prompt.format(country1="대한민국"))
print()


def get_today() -> str:
    return datetime.now().strftime("%B %d")


birthday_prompt = PromptTemplate(
    template="오늘의 날짜는 {today} 입니다. 오늘이 생일인 유명인 {n}명을 나열해 주세요.",
    input_variables=["n"],
    partial_variables={"today": get_today},
)

print("[callable-partial]")
print((birthday_prompt | llm | StrOutputParser()).invoke(3))
print()

file_prompt = load_prompt(str(PROJECT_ROOT / "02-Prompt" / "prompts" / "fruit_color.yaml"))
print("[load_prompt]")
print(file_prompt.format(fruit="사과"))
print()

chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "당신은 친절한 AI 어시스턴트입니다. 이름은 {name} 입니다."),
        ("human", "반가워요!"),
        ("ai", "안녕하세요! 무엇을 도와드릴까요?"),
        ("human", "{user_input}"),
    ]
)
print("[chat]")
print(
    (chat_prompt | llm | StrOutputParser()).invoke(
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
            "word_count": 5,
            "conversation": [
                ("human", "안녕하세요! 저는 오늘 새로 입사했습니다."),
                ("ai", "반갑습니다. 앞으로 잘 부탁드립니다."),
            ],
        }
    )
)
