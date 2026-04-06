from __future__ import annotations

import sys
from pathlib import Path

from langchain.tools import tool

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model


@tool
def issue_refund(order_id: str, amount: int) -> str:
    """Issue a refund for a customer order."""
    return f"refund issued: {order_id} / {amount}"


approval_policy = {"issue_refund": False}
model = make_chat_model(temperature=0).bind_tools([issue_refund])

response = model.invoke(
    "주문 ORD-103의 배송이 늦었으니 5000원 환불을 처리해줘."
)

for tool_call in response.tool_calls:
    approved = approval_policy.get(tool_call["name"], False)
    print(f"tool={tool_call['name']} approved={approved}")
    if approved:
        print(issue_refund.invoke(tool_call["args"]))
    else:
        print("human review required")
