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
embeddings = make_local_embeddings()

nlp_docs = splitter.split_documents(load_text_document(data_dir / "nlp-keywords.txt"))
finance_docs = splitter.split_documents(load_text_document(data_dir / "finance-keywords.txt"))

store = InMemoryVectorStore.from_documents(nlp_docs, embedding=embeddings)

extra_ids = store.add_documents(
    [
        Document(
            page_content="이번엔 텍스트 데이터를 추가합니다.",
            metadata={"source": "mydata.txt"},
        ),
        Document(
            page_content="추가한 두 번째 텍스트 데이터입니다.",
            metadata={"source": "mydata.txt"},
        ),
    ],
    ids=["extra_doc_1", "extra_doc_2"],
)
print(extra_ids)

for doc, score in store.similarity_search_with_score("TF IDF 에 대하여 알려줘", k=2):
    print(score)
    print(doc.metadata)
    print(doc.page_content[:200])
    print("=" * 30)

store.add_documents(finance_docs)
retriever = store.as_retriever(search_kwargs={"k": 3})
for doc in retriever.invoke("Word2Vec 와 ESG 를 각각 설명해줘"):
    print(doc.metadata)
    print(doc.page_content[:200])
    print("=" * 30)
