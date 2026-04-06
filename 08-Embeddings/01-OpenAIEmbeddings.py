from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.embedding_utils import cosine_similarity
from langchain_cookbook.example_utils import make_local_embeddings

embeddings = make_local_embeddings()

text = "임베딩 테스트를 위한 샘플 문장입니다."
query_result = embeddings.embed_query(text)
document_results = embeddings.embed_documents([text, text, text, text])

print(len(query_result))
print(len(document_results))
print(len(document_results[0]))

sentences = [
    "안녕하세요? 반갑습니다.",
    "안녕하세요? 반갑습니다!",
    "안녕하세요? 만나서 반가워요.",
    "Hi, nice to meet you.",
    "I like to eat apples.",
]
embedded_sentences = embeddings.embed_documents(sentences)

for index, vector in enumerate(embedded_sentences):
    for other_index, other_vector in enumerate(embedded_sentences):
        if index < other_index:
            score = cosine_similarity(vector, other_vector)
            print(
                f"[유사도 {score:.4f}] {sentences[index]} <=====> {sentences[other_index]}"
            )
