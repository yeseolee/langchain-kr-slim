from __future__ import annotations

from langchain_text_splitters import HTMLHeaderTextSplitter, RecursiveCharacterTextSplitter

html_string = """
<!DOCTYPE html>
<html>
<body>
    <div>
        <h1>헤더1</h1>
        <p>헤더1 에 포함된 본문</p>
        <div>
            <h2>헤더2-1 제목</h2>
            <p>헤더2-1 에 포함된 본문</p>
            <h3>헤더3-1 제목</h3>
            <p>헤더3-1 에 포함된 본문</p>
        </div>
        <div>
            <h2>헤더2-2 제목</h2>
            <p>헤더2-2 에 포함된 본문</p>
        </div>
    </div>
</body>
</html>
"""

headers_to_split_on = [
    ("h1", "Header 1"),
    ("h2", "Header 2"),
    ("h3", "Header 3"),
]

header_splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
header_docs = header_splitter.split_text(html_string)

for doc in header_docs:
    print(doc.page_content)
    print(doc.metadata)
    print("=" * 30)

chunk_splitter = RecursiveCharacterTextSplitter(chunk_size=80, chunk_overlap=10)
chunks = chunk_splitter.split_documents(header_docs)

for chunk in chunks:
    print(chunk.page_content)
    print(chunk.metadata)
    print("=" * 30)
