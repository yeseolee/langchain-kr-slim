from __future__ import annotations

from langsmith_helpers import (
    answer_with_context,
    create_grounded_dataset,
    groundedness,
    make_langsmith_client,
)

client = make_langsmith_client()
dataset_name = create_grounded_dataset(client, prefix="ported-groundedness")
results = client.evaluate(
    answer_with_context,
    data=dataset_name,
    evaluators=[groundedness],
    experiment_prefix="groundedness",
    upload_results=True,
)

print(results)
