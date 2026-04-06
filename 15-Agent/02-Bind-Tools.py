from __future__ import annotations

import sys
from pathlib import Path

from langchain.tools import tool

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model


@tool
def get_word_length(word: str) -> int:
    """Return the length of a word."""
    return len(word)


@tool
def add_function(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


tools = [get_word_length, add_function]
llm_with_tools = make_chat_model(temperature=0).bind_tools(tools)

response = llm_with_tools.invoke("What is the length of the word 'teddynote'?")
print(response.tool_calls)

for tool_call in response.tool_calls:
    matching_tool = next(tool for tool in tools if tool.name == tool_call["name"])
    print(matching_tool.invoke(tool_call["args"]))
