from __future__ import annotations

import base64
import sys
from pathlib import Path

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.openrouter_setup import load_openrouter_settings
from langchain_cookbook.service_utils import get_env


settings = load_openrouter_settings()
sample_png = (
    "iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAYAAABytg0kAAAAFElEQVR4nGP8z8Dwn4GBgYGJ"
    "AAAJYQG6dD0zLQAAAABJRU5ErkJggg=="
)

model = ChatOpenAI(
    model=get_env("OPENROUTER_MULTIMODAL_MODEL", "openai/gpt-4o-mini"),
    base_url=settings.base_url,
    api_key=settings.api_key,
    temperature=0,
)

message = HumanMessage(
    content=[
        {"type": "text", "text": "이미지에서 보이는 특징을 한 문장으로 설명해줘."},
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{sample_png}"},
        },
    ]
)

response = model.invoke([message])
print(response.content)
