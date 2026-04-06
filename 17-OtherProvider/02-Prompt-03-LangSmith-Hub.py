from __future__ import annotations

from langsmith_helpers import make_langsmith_client

client = make_langsmith_client()
prompt_identifier = "rlm/rag-prompt"
prompt = client.pull_prompt(prompt_identifier)

print(prompt_identifier)
print(prompt)
