from __future__ import annotations

import sys
from operator import itemgetter
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.document_utils import load_text_document
from langchain_cookbook.example_utils import make_chat_model
from langchain_cookbook.rag_utils import build_inmemory_store, format_docs

data_path = Path(__file__).resolve().parent / "data" / "appendix-keywords.txt"
documents = load_text_document(data_path)
_, store = build_inmemory_store(documents)
retriever = store.as_retriever(search_kwargs={"k": 2})

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "문맥을 사용해 질문에 답하세요."),
        ("human", "질문: {question}\n\n문맥:\n{context}"),
    ]
)

chain = (
    RunnablePassthrough.assign(
        context=itemgetter("question") | retriever | RunnableLambda(format_docs)
    )
    | prompt
    | make_chat_model(temperature=0)
    | StrOutputParser()
)

print(chain.invoke({"question": "TF-IDF 가 무엇인지 설명해줘"}))
