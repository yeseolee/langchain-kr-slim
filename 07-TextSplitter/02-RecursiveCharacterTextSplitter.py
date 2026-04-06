from __future__ import annotations

from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

data_path = Path(__file__).resolve().parent / "data" / "appendix-keywords.txt"
text = data_path.read_text(encoding="utf-8")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=250,
    chunk_overlap=50,
    length_function=len,
    is_separator_regex=False,
)
documents = splitter.create_documents([text])

print(documents[0].page_content)
print("=" * 60)
print(documents[1].page_content)
