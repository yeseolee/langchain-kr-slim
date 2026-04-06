from __future__ import annotations

import csv
import json
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

from langchain_core.documents import Document


class _HTMLTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        stripped = data.strip()
        if stripped:
            self.parts.append(stripped)

    def get_text(self) -> str:
        return "\n".join(self.parts)


def load_text_document(path: str | Path, *, encoding: str = "utf-8") -> list[Document]:
    file_path = Path(path)
    return [
        Document(
            page_content=file_path.read_text(encoding=encoding),
            metadata={"source": str(file_path)},
        )
    ]


def load_csv_documents(path: str | Path) -> list[Document]:
    file_path = Path(path)
    with file_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return [
            Document(
                page_content="\n".join(f"{key}: {value}" for key, value in row.items()),
                metadata={"source": str(file_path), "row": index},
            )
            for index, row in enumerate(reader, start=1)
        ]


def load_json_documents(path: str | Path) -> list[Document]:
    file_path = Path(path)
    data = json.loads(file_path.read_text(encoding="utf-8"))

    if isinstance(data, list):
        items = data
    else:
        items = [data]

    documents: list[Document] = []
    for index, item in enumerate(items, start=1):
        documents.append(
            Document(
                page_content=json.dumps(item, ensure_ascii=False, indent=2),
                metadata={"source": str(file_path), "index": index},
            )
        )
    return documents


def load_html_document(path: str | Path) -> list[Document]:
    file_path = Path(path)
    parser = _HTMLTextExtractor()
    parser.feed(file_path.read_text(encoding="utf-8"))
    return [
        Document(
            page_content=parser.get_text(),
            metadata={"source": str(file_path)},
        )
    ]


def load_directory_documents(directory: str | Path) -> list[Document]:
    base_dir = Path(directory)
    documents: list[Document] = []

    for path in sorted(base_dir.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix == ".txt":
            documents.extend(load_text_document(path))
        elif path.suffix == ".csv":
            documents.extend(load_csv_documents(path))
        elif path.suffix == ".json":
            documents.extend(load_json_documents(path))
        elif path.suffix in {".html", ".htm"}:
            documents.extend(load_html_document(path))

    return documents


__all__ = [
    "load_csv_documents",
    "load_directory_documents",
    "load_html_document",
    "load_json_documents",
    "load_text_document",
]
