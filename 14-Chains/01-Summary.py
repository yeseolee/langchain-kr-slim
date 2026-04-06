from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model

data_path = Path(__file__).resolve().parent / "data" / "news.txt"
source_text = data_path.read_text(encoding="utf-8")

splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=100)
chunks = splitter.split_text(source_text)

map_prompt = PromptTemplate.from_template(
    "다음 뉴스 조각을 2문장으로 요약하세요.\n\n{text}"
)
reduce_prompt = PromptTemplate.from_template(
    "다음 요약들을 종합해 최종 요약 3문장을 작성하세요.\n\n{summaries}"
)
llm = make_chat_model(temperature=0)

map_chain = map_prompt | llm | StrOutputParser()
reduce_chain = reduce_prompt | llm | StrOutputParser()

partial_summaries = [map_chain.invoke({"text": chunk}) for chunk in chunks]
final_summary = reduce_chain.invoke({"summaries": "\n\n".join(partial_summaries)})

print(final_summary)
