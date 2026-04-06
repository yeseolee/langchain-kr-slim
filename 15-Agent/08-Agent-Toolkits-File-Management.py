from __future__ import annotations

import sys
from pathlib import Path

from langchain.agents import create_agent
from langchain.tools import tool

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model


working_dir = Path(__file__).resolve().parent / "tmp"
working_dir.mkdir(exist_ok=True)
(working_dir / "todo.txt").write_text("보고서 초안 작성\n회의 일정 확인", encoding="utf-8")


@tool
def list_files() -> str:
    """List files under the working directory."""
    return "\n".join(sorted(path.name for path in working_dir.iterdir()))


@tool
def read_file(file_name: str) -> str:
    """Read a UTF-8 text file from the working directory."""
    return (working_dir / file_name).read_text(encoding="utf-8")


@tool
def write_file(file_name: str, content: str) -> str:
    """Write a UTF-8 text file to the working directory."""
    (working_dir / file_name).write_text(content, encoding="utf-8")
    return f"saved {file_name}"


agent = create_agent(
    model=make_chat_model(temperature=0),
    tools=[list_files, read_file, write_file],
    system_prompt="Only work inside the provided tmp directory.",
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "todo.txt 를 읽고 한 줄 요약 파일 summary.txt 로 저장해줘.",
            }
        ]
    }
)
print(result["messages"][-1].content)
