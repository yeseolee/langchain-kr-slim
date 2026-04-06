from __future__ import annotations

import csv
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.embedding_utils import cosine_similarity
from langchain_cookbook.example_utils import make_local_embeddings
from myrag import LocalTextRAG


def lexical_overlap(left: str, right: str) -> float:
    left_terms = {term for term in left.lower().split() if term}
    right_terms = {term for term in right.lower().split() if term}
    if not left_terms or not right_terms:
        return 0.0
    return len(left_terms & right_terms) / len(left_terms | right_terms)


data_dir = Path(__file__).resolve().parent / "data"
dataset_path = data_dir / "rag_eval.csv"
results_path = data_dir / "rag_eval_results.csv"
rag = LocalTextRAG(str(data_dir / "appendix-keywords.txt"))
embeddings = make_local_embeddings()

rows = list(csv.DictReader(dataset_path.open(encoding="utf-8")))
results: list[dict[str, object]] = []

for row in rows:
    prediction = rag.ask(row["question"])
    answer_similarity = cosine_similarity(
        embeddings.embed_query(prediction["answer"]),
        embeddings.embed_query(row["ground_truth"]),
    )
    context_joined = "\n".join(prediction["contexts"])
    context_overlap = lexical_overlap(context_joined, row["ground_truth"])
    results.append(
        {
            "question": row["question"],
            "ground_truth": row["ground_truth"],
            "answer": prediction["answer"],
            "answer_similarity": round(answer_similarity, 4),
            "context_overlap": round(context_overlap, 4),
        }
    )

with results_path.open("w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "question",
            "ground_truth",
            "answer",
            "answer_similarity",
            "context_overlap",
        ],
    )
    writer.writeheader()
    writer.writerows(results)

avg_similarity = sum(float(row["answer_similarity"]) for row in results) / len(results)
avg_overlap = sum(float(row["context_overlap"]) for row in results) / len(results)

print(f"avg_answer_similarity={avg_similarity:.4f}")
print(f"avg_context_overlap={avg_overlap:.4f}")
print(results_path)
