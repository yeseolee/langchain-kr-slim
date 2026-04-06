from __future__ import annotations

import sys
from operator import itemgetter
from pathlib import Path

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.document_utils import load_text_document
from langchain_cookbook.example_utils import make_chat_model
from langchain_cookbook.rag_utils import build_inmemory_store, format_docs

data_path = Path(__file__).resolve().parent / "data" / "appendix-keywords.txt"
documents = load_text_document(data_path)
_, store = build_inmemory_store(documents, chunk_size=300, chunk_overlap=40)
retriever = store.as_retriever(search_kwargs={"k": 3})

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "주어진 문맥과 대화 기록을 사용해 질문에 답하세요."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "질문: {question}\n\n문맥:\n{context}"),
    ]
)

rag_chain = (
    {
        "question": itemgetter("question"),
        "context": itemgetter("question") | retriever | RunnableLambda(format_docs),
        "chat_history": itemgetter("chat_history"),
    }
    | prompt
    | make_chat_model(temperature=0)
    | StrOutputParser()
)

store_by_session: dict[str, InMemoryChatMessageHistory] = {}


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store_by_session:
        store_by_session[session_id] = InMemoryChatMessageHistory()
    return store_by_session[session_id]


chain_with_history = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="chat_history",
)

config = {"configurable": {"session_id": "rag-demo"}}
print(chain_with_history.invoke({"question": "Word2Vec 이 무엇인가요?"}, config=config))
print(chain_with_history.invoke({"question": "방금 설명한 개념의 핵심 장점은?"}, config=config))
