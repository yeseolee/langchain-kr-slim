from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from langchain.agents import create_agent
from langchain.tools import tool

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model


dataframe = pd.read_csv(Path(__file__).resolve().parent / "data" / "titanic.csv")


@tool
def show_schema() -> str:
    """Return dataframe columns and dtypes."""
    return "\n".join(f"{column}: {dtype}" for column, dtype in dataframe.dtypes.items())


@tool
def preview_rows(limit: int = 5) -> str:
    """Return top rows from the dataframe."""
    return dataframe.head(limit).to_markdown(index=False)


@tool
def filter_count(column: str, value: str) -> int:
    """Count rows where a column exactly matches a value."""
    series = dataframe[column].astype(str).str.lower()
    return int((series == value.lower()).sum())


@tool
def aggregate_mean(column: str) -> float:
    """Return the mean of a numeric column."""
    return float(dataframe[column].mean())


agent = create_agent(
    model=make_chat_model(temperature=0),
    tools=[show_schema, preview_rows, filter_count, aggregate_mean],
    system_prompt=(
        "Use the dataframe tools to answer questions about the Titanic table. "
        "Cite the tool outputs directly and stay concise."
    ),
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "남성 승객 수와 전체 승객 평균 나이를 알려줘.",
            }
        ]
    }
)
print(result["messages"][-1].content)
