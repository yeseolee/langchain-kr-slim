from __future__ import annotations

from langchain_text_splitters import Language, RecursiveCharacterTextSplitter

python_code = """
def hello_world():
    print("Hello, World!")

hello_world()
"""

python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=50,
    chunk_overlap=0,
)
python_docs = python_splitter.create_documents([python_code])

for doc in python_docs:
    print(doc.page_content)
    print("=" * 30)

markdown_text = """
# LangChain

## 빠른 설치

```bash
pip install langchain
```

## 소개

LLM 애플리케이션을 구성 가능한 컴포넌트로 작성합니다.
"""

markdown_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.MARKDOWN,
    chunk_size=60,
    chunk_overlap=0,
)
markdown_docs = markdown_splitter.create_documents([markdown_text])

for doc in markdown_docs:
    print(doc.page_content)
    print("=" * 30)
