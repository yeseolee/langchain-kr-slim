from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "당신은 Question-Answering 챗봇입니다. 주어진 질문에 답변하세요.",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "#Question:\n{question}"),
    ]
)
chain = prompt | make_chat_model(temperature=0) | StrOutputParser()

store: dict[str, InMemoryChatMessageHistory] = {}


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="chat_history",
)

config = {"configurable": {"session_id": "abc123"}}
print(chain_with_history.invoke({"question": "나의 이름은 테디입니다."}, config=config))
print(chain_with_history.invoke({"question": "내 이름이 뭐라고?"}, config=config))

other_config = {"configurable": {"session_id": "abc1234"}}
print(chain_with_history.invoke({"question": "내 이름이 뭐라고?"}, config=other_config))
