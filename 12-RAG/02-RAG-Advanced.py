from __future__ import annotations

import sys
from operator import itemgetter
from pathlib import Path

from langchain_core.output_parsers import CommaSeparatedListOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnableLambda

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

query_parser = CommaSeparatedListOutputParser()
query_prompt = PromptTemplate(
    template=(
        "다음 질문을 검색용 대체 질의 3개로 바꿔주세요.\n"
        "{format_instructions}\n"
        "질문: {question}"
    ),
    input_variables=["question"],
    partial_variables={
        "format_instructions": query_parser.get_format_instructions(),
    },
)
query_chain = query_prompt | make_chat_model(temperature=0) | query_parser


def retrieve_multiquery(question: str) -> str:
    queries = query_chain.invoke({"question": question})
    seen_contents: set[str] = set()
    collected_docs = []
    for query in queries:
        for doc in store.similarity_search(query, k=2):
            if doc.page_content in seen_contents:
                continue
            seen_contents.add(doc.page_content)
            collected_docs.append(doc)
    return format_docs(collected_docs)


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "주어진 문맥만 사용해 질문에 답하세요. 모르면 모른다고 답하세요."),
        ("human", "질문: {question}\n\n문맥:\n{context}"),
    ]
)

chain = (
    {
        "question": itemgetter("question"),
        "context": itemgetter("question") | RunnableLambda(retrieve_multiquery),
    }
    | prompt
    | make_chat_model(temperature=0)
    | StrOutputParser()
)

print(chain.invoke({"question": "Word2Vec 과 TF-IDF 의 차이를 설명해줘"}))
