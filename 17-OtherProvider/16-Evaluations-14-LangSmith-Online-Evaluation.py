from __future__ import annotations

import uuid

from langsmith_helpers import make_langsmith_client, unique_name

client = make_langsmith_client()
project_name = unique_name("ported-online-eval")
trace_id = uuid.uuid4()
run_id = uuid.uuid4()

client.create_run(
    name="online-answer",
    run_type="chain",
    project_name=project_name,
    inputs={"question": "RAG의 목적은 무엇인가요?"},
    outputs={"answer": "검색된 문맥을 함께 제공해 답변 품질을 높입니다."},
    run_id=run_id,
    trace_id=trace_id,
)
feedback = client.create_feedback(
    run_id=run_id,
    trace_id=trace_id,
    key="groundedness",
    score=1.0,
    comment="manual online feedback",
)

print(project_name)
print(feedback.id)
