from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model

chain = (
    PromptTemplate.from_template("{topic} 에 대해 한 문장으로 설명하세요.")
    | make_chat_model(temperature=0)
    | StrOutputParser()
)

print(chain.input_schema.model_json_schema())
print(chain.output_schema.model_json_schema())
print(list(chain.get_graph().nodes.keys()))
