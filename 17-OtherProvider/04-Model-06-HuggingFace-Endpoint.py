from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.service_utils import get_env, require_env


llm = HuggingFaceEndpoint(
    model=get_env("HF_ENDPOINT_MODEL", "HuggingFaceH4/zephyr-7b-beta"),
    huggingfacehub_api_token=require_env("HUGGINGFACEHUB_API_TOKEN"),
    task="text-generation",
    max_new_tokens=256,
    temperature=0.2,
)
prompt = PromptTemplate.from_template("{question}")
chain = prompt | llm

print(chain.invoke({"question": "LangChain의 핵심 개념을 짧게 설명해줘."}))
