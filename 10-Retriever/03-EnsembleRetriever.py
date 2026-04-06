from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.document_utils import load_text_document
from langchain_cookbook.example_utils import make_local_embeddings


def keyword_search(documents: list[Document], query: str, k: int) -> list[Document]:
    query_terms = {term for term in query.lower().split() if term}
    scored: list[tuple[int, Document]] = []
    for doc in documents:
        score = sum(term in doc.page_content.lower() for term in query_terms)
        if score:
            scored.append((score, doc))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in scored[:k]]


data_path = Path(__file__).resolve().parent / "data" / "appendix-keywords.txt"
documents = load_text_document(data_path)
splitter = RecursiveCharacterTextSplitter(chunk_size=350, chunk_overlap=40)
chunks = splitter.split_documents(documents)

store = InMemoryVectorStore.from_documents(chunks, embedding=make_local_embeddings())
vector_docs = store.similarity_search("멀티모달 검색", k=3)
keyword_docs = keyword_search(chunks, "멀티모달 검색", k=3)

scores: dict[str, float] = defaultdict(float)
doc_map: dict[str, Document] = {}

for rank, doc in enumerate(vector_docs, start=1):
    key = doc.page_content
    doc_map[key] = doc
    scores[key] += 1 / rank

for rank, doc in enumerate(keyword_docs, start=1):
    key = doc.page_content
    doc_map[key] = doc
    scores[key] += 1 / rank

ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
for key, score in ranked[:3]:
    print(score)
    print(doc_map[key].page_content[:220])
    print("=" * 30)
