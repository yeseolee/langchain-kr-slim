from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_local_embeddings


def reorder_long_context(documents: list[Document]) -> list[Document]:
    front: list[Document] = []
    back: list[Document] = []
    for index, document in enumerate(documents):
        if index % 2 == 0:
            front.append(document)
        else:
            back.append(document)
    return front + list(reversed(back))


texts = [
    "이 문서는 일반적인 메모입니다.",
    "ChatGPT 는 사용자 질문에 답하도록 설계된 대화형 AI 시스템입니다.",
    "애플은 아이폰, 아이패드, 맥북 제품군을 보유하고 있습니다.",
    "ChatGPT 는 OpenAI가 개발했으며 추론과 요약에 자주 사용됩니다.",
    "ChatGPT 는 코드 작성, 문서 요약, 검색 보조에 활용됩니다.",
    "비트코인은 가치 저장 수단으로 자주 언급됩니다.",
]

documents = [
    Document(page_content=text, metadata={"rank": index})
    for index, text in enumerate(texts, start=1)
]
store = InMemoryVectorStore.from_documents(documents, embedding=make_local_embeddings())
ranked = store.similarity_search("ChatGPT 특징 설명", k=6)
reordered = reorder_long_context(ranked)

print("before")
for document in ranked:
    print(document.page_content)
print("=" * 30)
print("after")
for document in reordered:
    print(document.page_content)
