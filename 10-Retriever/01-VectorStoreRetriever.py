from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

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

store = InMemoryVectorStore.from_documents(chunks, embedding=make_local_embeddings())
retriever = store.as_retriever(search_kwargs={"k": 3})

for doc in retriever.invoke("Word2Vec 에 대하여 알려줘"):
    print(doc.metadata)
    print(doc.page_content[:220])
    print("=" * 30)
