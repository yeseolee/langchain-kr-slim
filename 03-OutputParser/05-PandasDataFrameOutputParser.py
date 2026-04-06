from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model


class DataFramePlan(BaseModel):
    filter_column: str | None = Field(default=None)
    filter_operator: str | None = Field(default=None)
    filter_value: str | None = Field(default=None)
    sort_by: str | None = Field(default=None)
    ascending: bool = Field(default=True)
    aggregation: str = Field(description="count, sum, mean, max, min 중 하나")
    target_column: str = Field(description="집계할 컬럼 이름")


def apply_plan(dataframe: pd.DataFrame, plan: DataFramePlan) -> object:
    working = dataframe.copy()

    if plan.filter_column and plan.filter_operator and plan.filter_value is not None:
        value: object = plan.filter_value
        if plan.filter_column in {"units", "price"}:
            value = float(plan.filter_value)

        if plan.filter_operator == "eq":
            working = working[working[plan.filter_column] == value]
        elif plan.filter_operator == "ge":
            working = working[working[plan.filter_column] >= value]
        elif plan.filter_operator == "contains":
            working = working[
                working[plan.filter_column].astype(str).str.contains(str(value))
            ]

    if plan.sort_by:
        working = working.sort_values(plan.sort_by, ascending=plan.ascending)

    series = working[plan.target_column]
    if plan.aggregation == "count":
        return int(series.count())
    if plan.aggregation == "sum":
        return float(series.sum())
    if plan.aggregation == "mean":
        return float(series.mean())
    if plan.aggregation == "max":
        return series.max()
    if plan.aggregation == "min":
        return series.min()
    raise ValueError(f"지원하지 않는 aggregation: {plan.aggregation}")


sales_df = pd.DataFrame(
    [
        {"product": "노트북", "category": "전자기기", "units": 18, "price": 1800000},
        {"product": "태블릿", "category": "전자기기", "units": 25, "price": 950000},
        {"product": "키보드", "category": "주변기기", "units": 40, "price": 120000},
        {"product": "마우스", "category": "주변기기", "units": 55, "price": 80000},
    ]
)

parser = PydanticOutputParser(pydantic_object=DataFramePlan)
prompt = PromptTemplate.from_template(
    """
질문을 판다스 실행 계획으로 변환하세요.

테이블 컬럼:
{columns}

샘플 데이터:
{sample}

질문:
{question}

응답 형식:
{format_instructions}
"""
).partial(format_instructions=parser.get_format_instructions())

question = "전자기기 카테고리 상품 중 평균 가격을 계산해줘."
chain = prompt | make_chat_model(temperature=0) | parser
plan = chain.invoke(
    {
        "columns": ", ".join(sales_df.columns),
        "sample": sales_df.to_json(orient="records", force_ascii=False),
        "question": question,
    }
)

result = apply_plan(sales_df, plan)
print(plan.model_dump_json(indent=2, ensure_ascii=False))
print(json.dumps({"question": question, "result": result}, ensure_ascii=False, indent=2))
