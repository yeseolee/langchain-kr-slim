from __future__ import annotations

from langsmith_helpers import answer_question, create_qa_dataset, make_langsmith_client


def summary_evaluator(outputs: list[dict], reference_outputs: list[dict]) -> dict:
    del reference_outputs
    avg_length = sum(len(output["answer"]) for output in outputs) / max(1, len(outputs))
    return {"key": "average_answer_length", "score": avg_length}


client = make_langsmith_client()
dataset_name = create_qa_dataset(client, prefix="ported-summary")
results = client.evaluate(
    answer_question,
    data=dataset_name,
    evaluators=[],
    summary_evaluators=[summary_evaluator],
    experiment_prefix="summary-eval",
    upload_results=True,
)

print(results)
