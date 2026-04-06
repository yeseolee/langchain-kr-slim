from __future__ import annotations

from langsmith_helpers import (
    answer_question,
    create_qa_dataset,
    embedding_similarity,
    make_langsmith_client,
)

client = make_langsmith_client()
dataset_name = create_qa_dataset(client, prefix="ported-embedding-distance")
results = client.evaluate(
    answer_question,
    data=dataset_name,
    evaluators=[embedding_similarity],
    experiment_prefix="embedding-distance",
    upload_results=True,
)

print(results)
