from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_core.prompts import PromptTemplate

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model

output_parser = CommaSeparatedListOutputParser()
prompt = PromptTemplate(
    template="List five {subject}.\n{format_instructions}",
    input_variables=["subject"],
    partial_variables={
        "format_instructions": output_parser.get_format_instructions(),
    },
)

chain = prompt | make_chat_model(temperature=0) | output_parser
response = chain.invoke({"subject": "대한민국 관광명소"})

print(response)
