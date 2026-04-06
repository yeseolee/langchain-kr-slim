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


data_path = Path(__file__).resolve().parent / "data" / "ai-story.txt"
parent_docs = RecursiveCharacterTextSplitter(chunk_size=450, chunk_overlap=50).split_documents(
    load_text_document(data_path)
)

summary_prompt = PromptTemplate.from_template(
    "다음 문단의 핵심 주제를 한 문장으로 요약하세요.\n\n{text}"
)
summary_chain = summary_prompt | make_chat_model(temperature=0)

summary_docs: list[Document] = []
parent_map: dict[str, Document] = {}
for index, parent_doc in enumerate(parent_docs, start=1):
    parent_id = f"parent-{index}"
    summary = summary_chain.invoke({"text": parent_doc.page_content}).content
    summary_docs.append(Document(page_content=summary, metadata={"parent_id": parent_id}))
    parent_map[parent_id] = parent_doc

store = InMemoryVectorStore.from_documents(summary_docs, embedding=make_local_embeddings())
hits = store.similarity_search("AI 가 인간과 협업하는 장면", k=2)

for hit in hits:
    parent_doc = parent_map[hit.metadata["parent_id"]]
    print(hit.page_content)
    print(parent_doc.page_content[:400])
    print("=" * 30)
