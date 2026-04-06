from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.prompts import PromptTemplate

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model
from langsmith_helpers import create_qa_dataset, make_langsmith_client


prompt = PromptTemplate.from_template("질문에 한 문장으로 답하세요.\n\n{question}")


def answer_cold(inputs: dict) -> dict:
    return {"answer": (prompt | make_chat_model(temperature=0)).invoke(inputs).content}


def answer_warm(inputs: dict) -> dict:
    return {"answer": (prompt | make_chat_model(temperature=0.7)).invoke(inputs).content}


def pairwise(outputs: list[dict], reference_outputs: list[dict]) -> dict:
    del reference_outputs
    lengths = [len(item["answer"]) for item in outputs]
    return {"key": "pairwise_length_bias", "score": int(lengths[0] >= lengths[1])}


client = make_langsmith_client()
dataset_name = create_qa_dataset(client, prefix="ported-compare")
results = client.evaluate(
    (answer_cold, answer_warm),
    data=dataset_name,
    evaluators=[pairwise],
    experiment_prefix="compare",
    upload_results=True,
)

print(results)
