from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import CrossEncoder

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.document_utils import load_text_document
from langchain_cookbook.example_utils import make_local_embeddings

data_path = Path(__file__).resolve().parent / "data" / "appendix-keywords.txt"
documents = load_text_document(data_path)
splitter = RecursiveCharacterTextSplitter(chunk_size=350, chunk_overlap=40)
chunks = splitter.split_documents(documents)

query = "Word2Vec 이 임베딩과 어떻게 연결되는지 설명해줘"
store = InMemoryVectorStore.from_documents(chunks, embedding=make_local_embeddings())
retrieved_docs = store.similarity_search(query, k=5)

reranker = CrossEncoder("BAAI/bge-reranker-v2-m3")
scores = reranker.predict([(query, doc.page_content) for doc in retrieved_docs])

ranked = sorted(
    zip(scores, retrieved_docs, strict=True),
    key=lambda item: item[0],
    reverse=True,
)

for score, doc in ranked:
    print(float(score))
    print(doc.page_content[:240])
    print("=" * 30)
