from __future__ import annotations

import json
import sys
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model

chain = (
    PromptTemplate.from_template("{topic} 의 핵심 개념 3가지를 불렛 없이 짧게 설명하세요.")
    | make_chat_model(temperature=0)
    | StrOutputParser()
    | RunnableLambda(lambda text: json.dumps({"answer": text}, ensure_ascii=False))
)

print(chain.invoke({"topic": "LCEL"}))
