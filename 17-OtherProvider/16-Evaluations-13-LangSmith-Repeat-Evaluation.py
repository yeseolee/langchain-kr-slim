from __future__ import annotations

from langsmith_helpers import (
    answer_question,
    create_qa_dataset,
    make_langsmith_client,
    token_overlap,
)

client = make_langsmith_client()
dataset_name = create_qa_dataset(client, prefix="ported-repeat")
results = client.evaluate(
    answer_question,
    data=dataset_name,
    evaluators=[token_overlap],
    experiment_prefix="repeat",
    num_repetitions=3,
    upload_results=True,
)

print(results)
