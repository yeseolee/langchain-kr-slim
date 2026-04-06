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


def answer_a(inputs: dict) -> dict:
    return {"answer": (prompt | make_chat_model(temperature=0)).invoke(inputs).content}


def answer_b(inputs: dict) -> dict:
    return {"answer": (prompt | make_chat_model(temperature=0.4)).invoke(inputs).content}


def pairwise_evaluator(runs: list, example) -> dict:
    del example
    answers = [run.outputs["answer"] for run in runs]
    preferred = 0 if len(answers[0]) >= len(answers[1]) else 1
    return {"key": "pairwise_preference", "scores": {runs[preferred].id: 1}}


client = make_langsmith_client()
dataset_name = create_qa_dataset(client, prefix="ported-pairwise")
results = client.evaluate(
    (answer_a, answer_b),
    data=dataset_name,
    evaluators=[pairwise_evaluator],
    experiment_prefix="pairwise",
    upload_results=True,
)

print(results)
