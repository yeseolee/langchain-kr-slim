from __future__ import annotations

from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_cookbook.example_utils import make_local_embeddings


def format_docs(documents: list[Document]) -> str:
    return "\n\n".join(document.page_content for document in documents)


def build_inmemory_store(
    documents: list[Document],
    *,
    chunk_size: int = 400,
    chunk_overlap: int = 50,
) -> tuple[list[Document], InMemoryVectorStore]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunks = splitter.split_documents(documents)
    store = InMemoryVectorStore.from_documents(chunks, embedding=make_local_embeddings())
    return chunks, store


__all__ = ["build_inmemory_store", "format_docs"]
