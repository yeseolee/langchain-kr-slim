from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import ConfigurableField

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model


prompt = PromptTemplate.from_template("{topic}을 한 문단으로 설명하세요.")
model = make_chat_model(temperature=0).configurable_fields(
    temperature=ConfigurableField(
        id="response_temperature",
        name="Temperature",
        description="응답 다양성",
    )
)

chain = prompt | model
default_answer = chain.invoke({"topic": "RAG"}).content
creative_answer = chain.with_config(
    configurable={"response_temperature": 0.8}
).invoke({"topic": "RAG"}).content

print("default")
print(default_answer)
print("=" * 30)
print("creative")
print(creative_answer)
