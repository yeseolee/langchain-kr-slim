from __future__ import annotations

from langchain_core.prompts import PromptTemplate

from langsmith_helpers import make_langsmith_client

client = make_langsmith_client()
prompt_identifier = "your-name/summary-stuff-documents"
prompt = PromptTemplate.from_template(
    """
문서를 읽고 핵심만 불릿포인트로 요약하세요.

문서:
{context}
"""
)

commit_hash = client.push_prompt(
    prompt_identifier,
    object=prompt,
    is_public=False,
    description="Personal summary prompt",
)
print(commit_hash)
