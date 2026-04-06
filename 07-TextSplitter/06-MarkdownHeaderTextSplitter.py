from __future__ import annotations

from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

markdown_document = """
# Intro

## History

Markdown is a lightweight markup language for creating formatted text.

### Standardization

Many implementations appeared as the format became popular.

# Implementations

Markdown is supported by many programming languages and tools.
"""

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

header_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on,
    strip_headers=False,
)
header_docs = header_splitter.split_text(markdown_document)

for doc in header_docs:
    print(doc.page_content)
    print(doc.metadata)
    print("=" * 30)

chunk_splitter = RecursiveCharacterTextSplitter(chunk_size=120, chunk_overlap=20)
chunks = chunk_splitter.split_documents(header_docs)

for chunk in chunks:
    print(chunk.page_content)
    print(chunk.metadata)
    print("=" * 30)
