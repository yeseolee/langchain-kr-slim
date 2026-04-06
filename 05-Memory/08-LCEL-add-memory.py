from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model


class ChatHistoryChain:
    def __init__(self) -> None:
        self.history = InMemoryChatMessageHistory()
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful chatbot."),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]
        )
        self.chain = (
            RunnablePassthrough.assign(
                chat_history=RunnableLambda(lambda _: self.history.messages)
            )
            | prompt
            | make_chat_model(temperature=0)
            | StrOutputParser()
        )

    def invoke(self, user_text: str) -> str:
        answer = self.chain.invoke({"input": user_text})
        self.history.add_user_message(user_text)
        self.history.add_ai_message(answer)
        return answer


conversation = ChatHistoryChain()

print(conversation.invoke("안녕하세요. 제 이름은 테디입니다."))
print(conversation.invoke("제 이름이 무엇이었는지 기억하나요?"))
print(conversation.history.messages)
