from __future__ import annotations

import csv
import os
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_core.prompts import PromptTemplate
from langsmith import Client

from langchain_cookbook.embedding_utils import cosine_similarity
from langchain_cookbook.example_utils import make_chat_model, make_local_embeddings
from langchain_cookbook.service_utils import get_env, require_env


def make_langsmith_client() -> Client:
    return Client(
        api_key=require_env("LANGSMITH_API_KEY"),
        api_url=get_env("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com"),
    )


def unique_name(prefix: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{prefix}-{timestamp}"


def load_csv_examples(path: Path, *, limit: int = 3) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        rows = []
        for row in reader:
            rows.append(row)
            if len(rows) >= limit:
                break
    return rows


def create_qa_dataset(client: Client, *, prefix: str, limit: int = 3) -> str:
    dataset_name = unique_name(prefix)
    client.create_dataset(dataset_name=dataset_name, description="Ported QA examples")
    source_path = PROJECT_ROOT / "16-Evaluations" / "data" / "rag_eval.csv"
    examples = [
        {
            "inputs": {"question": row["question"]},
            "outputs": {"answer": row["ground_truth"]},
        }
        for row in load_csv_examples(source_path, limit=limit)
    ]
    client.create_examples(dataset_name=dataset_name, examples=examples)
    return dataset_name


def create_grounded_dataset(client: Client, *, prefix: str, limit: int = 3) -> str:
    dataset_name = unique_name(prefix)
    client.create_dataset(
        dataset_name=dataset_name,
        description="Groundedness examples with contexts",
    )
    source_path = PROJECT_ROOT / "17-OtherProvider" / "data" / "test_df_translated.csv"
    examples = []
    for row in load_csv_examples(source_path, limit=limit):
        examples.append(
            {
                "inputs": {
                    "question": row["question"],
                    "context": row["contexts"],
                },
                "outputs": {"answer": row["ground_truth"]},
            }
        )
    client.create_examples(dataset_name=dataset_name, examples=examples)
    return dataset_name


def answer_question(inputs: dict) -> dict:
    prompt = PromptTemplate.from_template(
        "질문에 한 문장으로 답하세요.\n\n질문: {question}"
    )
    chain = prompt | make_chat_model(temperature=0)
    return {"answer": chain.invoke(inputs).content}


def answer_with_context(inputs: dict) -> dict:
    prompt = PromptTemplate.from_template(
        """
주어진 문맥만 사용해 질문에 답하세요.

문맥:
{context}

질문:
{question}
"""
    )
    chain = prompt | make_chat_model(temperature=0)
    return {"answer": chain.invoke(inputs).content}


def exact_match(outputs: dict, reference_outputs: dict) -> dict:
    return {
        "key": "exact_match",
        "score": outputs["answer"].strip() == reference_outputs["answer"].strip(),
    }


def token_overlap(outputs: dict, reference_outputs: dict) -> dict:
    predicted = set(outputs["answer"].lower().split())
    expected = set(reference_outputs["answer"].lower().split())
    overlap = len(predicted & expected) / max(1, len(expected))
    return {"key": "token_overlap", "score": overlap}


def embedding_similarity(outputs: dict, reference_outputs: dict) -> dict:
    embeddings = make_local_embeddings()
    predicted = embeddings.embed_query(outputs["answer"])
    expected = embeddings.embed_query(reference_outputs["answer"])
    return {
        "key": "embedding_similarity",
        "score": cosine_similarity(predicted, expected),
    }


def groundedness(outputs: dict, inputs: dict) -> dict:
    answer_tokens = set(outputs["answer"].lower().split())
    context_tokens = set(inputs["context"].lower().split())
    score = len(answer_tokens & context_tokens) / max(1, len(answer_tokens))
    return {"key": "groundedness", "score": score}


def judge_answer(inputs: dict, outputs: dict, reference_outputs: dict) -> dict:
    prompt = PromptTemplate.from_template(
        """
정답과 모델 답변이 의미상 일치하면 YES, 아니면 NO 를 출력하세요.

질문:
{question}

정답:
{reference_answer}

모델 답변:
{predicted_answer}
"""
    )
    chain = prompt | make_chat_model(temperature=0)
    verdict = chain.invoke(
        {
            "question": inputs["question"],
            "reference_answer": reference_outputs["answer"],
            "predicted_answer": outputs["answer"],
        }
    ).content.strip()
    return {"key": "llm_judge", "score": verdict.upper().startswith("YES")}


__all__ = [
    "answer_question",
    "answer_with_context",
    "create_grounded_dataset",
    "create_qa_dataset",
    "embedding_similarity",
    "exact_match",
    "groundedness",
    "judge_answer",
    "make_langsmith_client",
    "token_overlap",
    "unique_name",
]
