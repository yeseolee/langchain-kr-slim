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


data_dir = Path(__file__).resolve().parent / "data"
tables = {
    "csv": pd.read_csv(data_dir / "titanic.csv"),
    "excel": pd.read_excel(data_dir / "titanic.xlsx"),
}


@tool
def list_tables() -> str:
    """List available table names."""
    return ", ".join(sorted(tables))


@tool
def table_schema(table_name: str) -> str:
    """Return schema for a table."""
    dataframe = tables[table_name]
    return "\n".join(f"{column}: {dtype}" for column, dtype in dataframe.dtypes.items())


@tool
def survival_rate(table_name: str, sex: str) -> float:
    """Return survival rate for a sex value in the selected table."""
    dataframe = tables[table_name]
    filtered = dataframe[dataframe["Sex"].str.lower() == sex.lower()]
    return float(filtered["Survived"].mean())


agent = create_agent(
    model=make_chat_model(temperature=0),
    tools=[list_tables, table_schema, survival_rate],
    system_prompt="Use the dataframe tools for CSV and Excel analysis.",
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "csv 와 excel 데이터에서 여성 생존률이 같은지 비교해줘.",
            }
        ]
    }
)
print(result["messages"][-1].content)
