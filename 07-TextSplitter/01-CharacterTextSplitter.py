from __future__ import annotations

from pathlib import Path

from langchain_text_splitters import CharacterTextSplitter

data_path = Path(__file__).resolve().parent / "data" / "appendix-keywords.txt"
text = data_path.read_text(encoding="utf-8")

splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=210,
    chunk_overlap=0,
    length_function=len,
)
documents = splitter.create_documents([text], metadatas=[{"document": 1}])

print(len(documents))
print(documents[0].metadata)
print(documents[0].page_content)
