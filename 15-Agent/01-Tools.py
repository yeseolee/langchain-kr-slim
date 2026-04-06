from __future__ import annotations

from pathlib import Path

from langchain.tools import tool


@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


@tool
def search_local_notes(query: str) -> str:
    """Search the local appendix note and return matching lines."""
    data_path = Path(__file__).resolve().parent / "data" / "appendix-keywords.txt"
    lines = data_path.read_text(encoding="utf-8").splitlines()
    matches = [line for line in lines if query.lower() in line.lower()]
    return "\n".join(matches[:5]) or "검색 결과가 없습니다."


print(add_numbers.name, add_numbers.description)
print(multiply_numbers.name, multiply_numbers.description)
print(search_local_notes.name, search_local_notes.description)

print(add_numbers.invoke({"a": 3, "b": 4}))
print(multiply_numbers.invoke({"a": 3, "b": 4}))
print(search_local_notes.invoke({"query": "Word2Vec"}))
