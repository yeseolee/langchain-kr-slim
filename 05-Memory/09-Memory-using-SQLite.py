from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables.utils import ConfigurableFieldSpec

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model
from langchain_cookbook.history_utils import SQLiteChatMessageHistory

db_path = Path(__file__).resolve().parent / "sqlite_history.db"

chat_message_history = SQLiteChatMessageHistory(
    session_id="sql_history",
    db_path=db_path,
    table_name="default_history",
)
chat_message_history.add_user_message(
    "안녕? 만나서 반가워. 내 이름은 테디야. 나는 랭체인 개발자야."
)
chat_message_history.add_ai_message("안녕 테디, 만나서 반가워.")
print(chat_message_history.messages)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)
chain = prompt | make_chat_model(temperature=0) | StrOutputParser()


def get_chat_history(user_id: str, conversation_id: str) -> SQLiteChatMessageHistory:
    return SQLiteChatMessageHistory(
        session_id=conversation_id,
        db_path=db_path,
        table_name=user_id,
    )


config_fields = [
    ConfigurableFieldSpec(
        id="user_id",
        annotation=str,
        name="User ID",
        description="Unique identifier for a user.",
        default="user1",
        is_shared=True,
    ),
    ConfigurableFieldSpec(
        id="conversation_id",
        annotation=str,
        name="Conversation ID",
        description="Unique identifier for a conversation.",
        default="conversation1",
        is_shared=True,
    ),
]

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_chat_history,
    input_messages_key="question",
    history_messages_key="chat_history",
    history_factory_config=config_fields,
)

config = {"configurable": {"user_id": "user1", "conversation_id": "conversation1"}}
print(chain_with_history.invoke({"question": "안녕, 내 이름은 테디야."}, config=config))
print(chain_with_history.invoke({"question": "내 이름이 뭐라고?"}, config=config))

other_config = {
    "configurable": {"user_id": "user1", "conversation_id": "conversation2"}
}
print(chain_with_history.invoke({"question": "내 이름이 뭐라고?"}, config=other_config))
