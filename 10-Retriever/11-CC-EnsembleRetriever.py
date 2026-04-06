from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

from kiwipiepy import Kiwi
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rank_bm25 import BM25Okapi

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.document_utils import load_text_document
from langchain_cookbook.example_utils import make_chat_model, make_local_embeddings


def compress(query: str, document: Document) -> str:
    prompt = PromptTemplate.from_template(
        """
질문과 직접 관련된 문장만 2문장 이하로 정리하세요.
관련이 없으면 IRRELEVANT 만 출력하세요.

질문:
{query}

문서:
{context}
"""
    )
    chain = prompt | make_chat_model(temperature=0)
    return chain.invoke({"query": query, "context": document.page_content}).content.strip()


kiwi = Kiwi()


def tokenize(text: str) -> list[str]:
    return [token.form for token in kiwi.tokenize(text) if token.form.strip()]


data_path = Path(__file__).resolve().parent / "data" / "appendix-keywords.txt"
chunks = RecursiveCharacterTextSplitter(chunk_size=260, chunk_overlap=40).split_documents(
    load_text_document(data_path)
)

store = InMemoryVectorStore.from_documents(chunks, embedding=make_local_embeddings())
vector_docs = store.similarity_search("Word2Vec 과 임베딩 차이", k=4)

bm25 = BM25Okapi([tokenize(chunk.page_content) for chunk in chunks])
bm25_scores = bm25.get_scores(tokenize("Word2Vec 과 임베딩 차이"))
keyword_docs = [
    document
    for _, document in sorted(
        zip(bm25_scores, chunks, strict=True),
        key=lambda item: item[0],
        reverse=True,
    )[:4]
]

scores: dict[str, float] = defaultdict(float)
doc_map: dict[str, Document] = {}
for rank, document in enumerate(vector_docs, start=1):
    scores[document.page_content] += 1 / rank
    doc_map[document.page_content] = document

for rank, document in enumerate(keyword_docs, start=1):
    scores[document.page_content] += 1 / rank
    doc_map[document.page_content] = document

for _, document_text in sorted(
    [(score, text) for text, score in scores.items()],
    key=lambda item: item[0],
    reverse=True,
)[:3]:
    compressed = compress("Word2Vec 과 임베딩 차이", doc_map[document_text])
    if compressed != "IRRELEVANT":
        print(compressed)
        print("-" * 30)
