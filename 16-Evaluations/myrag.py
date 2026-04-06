from __future__ import annotations

import sys
from dataclasses import dataclass
from operator import itemgetter
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.document_utils import load_text_document
from langchain_cookbook.example_utils import make_chat_model
from langchain_cookbook.rag_utils import build_inmemory_store, format_docs


@dataclass
class LocalTextRAG:
    file_path: str

    def __post_init__(self) -> None:
        documents = load_text_document(self.file_path)
        _, store = build_inmemory_store(documents, chunk_size=300, chunk_overlap=40)
        self.retriever = store.as_retriever(search_kwargs={"k": 3})
        self.chain = (
            {
                "question": itemgetter("question"),
                "context": itemgetter("question")
                | self.retriever
                | RunnableLambda(format_docs),
            }
            | ChatPromptTemplate.from_messages(
                [
                    ("system", "문맥만 사용해 질문에 답하세요."),
                    ("human", "질문: {question}\n\n문맥:\n{context}"),
                ]
            )
            | make_chat_model(temperature=0)
            | StrOutputParser()
        )

    def ask(self, question: str) -> dict[str, object]:
        contexts = self.retriever.invoke(question)
        answer = self.chain.invoke({"question": question})
        return {
            "question": question,
            "answer": answer,
            "contexts": [doc.page_content for doc in contexts],
        }
