from __future__ import annotations

import csv
import sys
from pathlib import Path

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model


class EvalItem(BaseModel):
    question: str = Field(description="평가용 질문")
    ground_truth: str = Field(description="질문에 대한 정답")


class EvalDataset(BaseModel):
    items: list[EvalItem] = Field(description="평가 데이터셋 항목 목록")


source_path = Path(__file__).resolve().parent / "data" / "appendix-keywords.txt"
output_path = Path(__file__).resolve().parent / "data" / "generated_eval_dataset.csv"
source_text = source_path.read_text(encoding="utf-8")

parser = PydanticOutputParser(pydantic_object=EvalDataset)
prompt = PromptTemplate.from_template(
    """
다음 문서를 읽고 평가용 질문-정답 쌍 5개를 생성하세요.

문서:
{source_text}

형식:
{format_instructions}
"""
).partial(format_instructions=parser.get_format_instructions())

chain = prompt | make_chat_model(temperature=0) | parser
dataset = chain.invoke({"source_text": source_text})

with output_path.open("w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["question", "ground_truth"])
    writer.writeheader()
    for item in dataset.items:
        writer.writerow(item.model_dump())

print(output_path)
