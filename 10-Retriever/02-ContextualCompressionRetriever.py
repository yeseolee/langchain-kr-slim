from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.document_utils import load_text_document
from langchain_cookbook.example_utils import make_chat_model, make_local_embeddings


def compress_document(query: str, document: Document) -> str:
    prompt = PromptTemplate.from_template(
        """
질문과 관련된 내용만 남겨 2문장 이하로 압축하세요.
관련 내용이 없으면 IRRELEVANT 라고만 답하세요.

질문:
{query}

문서:
{context}
"""
    )
    chain = prompt | make_chat_model(temperature=0)
    return chain.invoke({"query": query, "context": document.page_content}).content.strip()


data_path = Path(__file__).resolve().parent / "data" / "appendix-keywords.txt"
documents = load_text_document(data_path)
chunks = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=40).split_documents(
    documents
)

store = InMemoryVectorStore.from_documents(chunks, embedding=make_local_embeddings())
query = "Word2Vec 의 핵심 아이디어를 설명해줘."
retrieved = store.similarity_search(query, k=4)

for document in retrieved:
    compressed = compress_document(query, document)
    if compressed == "IRRELEVANT":
        continue
    print(compressed)
    print("-" * 30)
