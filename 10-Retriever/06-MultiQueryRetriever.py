from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.document_utils import load_text_document
from langchain_cookbook.example_utils import make_chat_model, make_local_embeddings

data_path = Path(__file__).resolve().parent / "data" / "appendix-keywords.txt"
documents = load_text_document(data_path)
splitter = RecursiveCharacterTextSplitter(chunk_size=350, chunk_overlap=40)
chunks = splitter.split_documents(documents)

store = InMemoryVectorStore.from_documents(chunks, embedding=make_local_embeddings())

query_parser = CommaSeparatedListOutputParser()
query_prompt = PromptTemplate(
    template=(
        "사용자 질문을 벡터 검색용으로 바꾼 대체 질의 3개를 생성하세요.\n"
        "{format_instructions}\n"
        "질문: {question}"
    ),
    input_variables=["question"],
    partial_variables={
        "format_instructions": query_parser.get_format_instructions(),
    },
)

query_chain = query_prompt | make_chat_model(temperature=0) | query_parser
generated_queries = query_chain.invoke({"question": "Word2Vec 과 임베딩 차이를 설명해줘"})

print(generated_queries)

seen_contents: set[str] = set()
for query in generated_queries:
    for doc in store.similarity_search(query, k=2):
        if doc.page_content in seen_contents:
            continue
        seen_contents.add(doc.page_content)
        print(f"[query] {query}")
        print(doc.page_content[:220])
        print("=" * 30)
