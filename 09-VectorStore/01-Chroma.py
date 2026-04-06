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

data_dir = Path(__file__).resolve().parent / "data"
splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=0)

nlp_docs = splitter.split_documents(load_text_document(data_dir / "nlp-keywords.txt"))
finance_docs = splitter.split_documents(load_text_document(data_dir / "finance-keywords.txt"))

store = InMemoryVectorStore.from_documents(nlp_docs, embedding=make_local_embeddings())

print("[similarity_search]")
for doc in store.similarity_search("TF IDF 에 대하여 알려줘", k=2):
    print(doc.metadata)
    print(doc.page_content[:200])
    print("=" * 30)

added_ids = store.add_documents(
    [
        Document(
            page_content="안녕하세요! 이번엔 도큐먼트를 새로 추가해 볼게요.",
            metadata={"source": "mydata.txt"},
        )
    ],
    ids=["new_doc_1"],
)
print(added_ids)
print(store.get_by_ids(["new_doc_1"]))

store.add_documents(finance_docs)
print("[retriever]")
retriever = store.as_retriever(search_kwargs={"k": 2})
for doc in retriever.invoke("ESG 에 대하여 알려줘"):
    print(doc.metadata)
    print(doc.page_content[:200])
    print("=" * 30)

store.delete(ids=["new_doc_1"])
print(store.get_by_ids(["new_doc_1"]))
