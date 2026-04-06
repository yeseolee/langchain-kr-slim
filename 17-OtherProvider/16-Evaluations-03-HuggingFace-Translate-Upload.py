from __future__ import annotations

import sys
from pathlib import Path

from datasets import Dataset
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model
from langchain_cookbook.service_utils import require_env


dataset = Dataset.from_csv(
    str(Path(__file__).resolve().parent / "data" / "test_df.csv")
).select(range(3))
translate_chain = (
    PromptTemplate.from_template("다음 질문을 한국어로 번역하세요.\n\n{question}")
    | make_chat_model(temperature=0)
    | StrOutputParser()
)

translated_questions = [translate_chain.invoke({"question": row["question"]}) for row in dataset]
translated_dataset = dataset.add_column("translated_question", translated_questions)

repo_id = require_env("HF_DATASET_REPO_ID")
translated_dataset.push_to_hub(repo_id, private=True)
print(repo_id)
