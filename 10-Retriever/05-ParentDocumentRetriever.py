from __future__ import annotations

import sys
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

data_path = Path(__file__).resolve().parent / "data" / "ai-story.txt"
base_documents = load_text_document(data_path)

parent_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
child_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=40)

parents = parent_splitter.split_documents(base_documents)
parent_map: dict[str, Document] = {}
child_documents: list[Document] = []

for index, parent in enumerate(parents, start=1):
    parent_id = f"parent-{index}"
    parent.metadata["parent_id"] = parent_id
    parent_map[parent_id] = parent
    for child in child_splitter.split_documents([parent]):
        child.metadata["parent_id"] = parent_id
        child_documents.append(child)

store = InMemoryVectorStore.from_documents(child_documents, embedding=make_local_embeddings())
child_hits = store.similarity_search("이야기 속 주인공의 갈등을 설명해줘", k=4)

seen_parent_ids: set[str] = set()
for child in child_hits:
    parent_id = child.metadata["parent_id"]
    if parent_id in seen_parent_ids:
        continue
    seen_parent_ids.add(parent_id)
    parent = parent_map[parent_id]
    print(parent.metadata)
    print(parent.page_content[:400])
    print("=" * 30)
