from __future__ import annotations

import sys
from pathlib import Path

from flashrank import Ranker, RerankRequest
from langchain_text_splitters import RecursiveCharacterTextSplitter

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.document_utils import load_text_document


data_path = Path(__file__).resolve().parent / "data" / "appendix-keywords.txt"
documents = RecursiveCharacterTextSplitter(chunk_size=450, chunk_overlap=80).split_documents(
    load_text_document(data_path)
)

passages = [
    {"id": str(index), "text": document.page_content, "meta": document.metadata}
    for index, document in enumerate(documents, start=1)
]

ranker = Ranker(model_name="ms-marco-MultiBERT-L-12")
request = RerankRequest(query="Word2Vec 에 대해 설명해줘.", passages=passages)
results = ranker.rerank(request)

for item in results[:3]:
    print(item["id"], round(float(item["score"]), 4))
    print(item["text"][:260])
    print("-" * 30)
