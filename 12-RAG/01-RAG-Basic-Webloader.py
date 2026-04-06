from __future__ import annotations

import sys
from operator import itemgetter
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.document_utils import load_html_document
from langchain_cookbook.example_utils import make_chat_model
from langchain_cookbook.rag_utils import build_inmemory_store, format_docs

data_path = Path(__file__).resolve().parent / "data" / "client.html"
documents = load_html_document(data_path)
_, store = build_inmemory_store(documents)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "주어진 HTML 문맥만 사용해 질문에 답하세요."),
        ("human", "질문: {question}\n\n문맥:\n{context}"),
    ]
)

retriever = store.as_retriever(search_kwargs={"k": 3})
chain = (
    {
        "question": itemgetter("question"),
        "context": itemgetter("question") | retriever | RunnableLambda(format_docs),
    }
    | prompt
    | make_chat_model(temperature=0)
    | StrOutputParser()
)

print(chain.invoke({"question": "페이지의 핵심 서비스 소개를 요약해줘"}))
