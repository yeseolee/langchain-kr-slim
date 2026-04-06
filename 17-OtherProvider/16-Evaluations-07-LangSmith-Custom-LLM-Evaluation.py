from __future__ import annotations

from langsmith_helpers import (
    answer_question,
    create_qa_dataset,
    make_langsmith_client,
    token_overlap,
)


def custom_evaluator(outputs: dict, reference_outputs: dict) -> dict:
    result = token_overlap(outputs, reference_outputs)
    result["key"] = "custom_overlap"
    result["comment"] = "Token overlap based custom evaluator"
    return result


client = make_langsmith_client()
dataset_name = create_qa_dataset(client, prefix="ported-custom-eval")
results = client.evaluate(
    answer_question,
    data=dataset_name,
    evaluators=[custom_evaluator],
    experiment_prefix="custom-evaluator",
    upload_results=True,
)

print(results)
