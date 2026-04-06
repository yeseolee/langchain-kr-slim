from __future__ import annotations

from langsmith_helpers import create_qa_dataset, make_langsmith_client

client = make_langsmith_client()
dataset_name = create_qa_dataset(client, prefix="ported-rag-dataset")

print(dataset_name)
