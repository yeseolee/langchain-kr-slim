from __future__ import annotations

from langsmith_helpers import (
    answer_question,
    create_qa_dataset,
    judge_answer,
    make_langsmith_client,
)

client = make_langsmith_client()
dataset_name = create_qa_dataset(client, prefix="ported-judge")
results = client.evaluate(
    answer_question,
    data=dataset_name,
    evaluators=[judge_answer],
    experiment_prefix="llm-judge",
    upload_results=True,
)

print(results)
