from __future__ import annotations

import sys
import time
from pathlib import Path

from langchain_text_splitters import CharacterTextSplitter

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.embedding_utils import DiskCachedEmbeddings
from langchain_cookbook.example_utils import DEFAULT_EMBEDDING_MODEL, make_local_embeddings

data_path = Path(__file__).resolve().parent / "data" / "appendix-keywords.txt"
cache_path = Path(__file__).resolve().parent / "cache" / "local_embeddings.json"

raw_text = data_path.read_text(encoding="utf-8")
splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=0)
documents = splitter.create_documents([raw_text])
texts = [document.page_content for document in documents]

cached_embeddings = DiskCachedEmbeddings(
    underlying_embeddings=make_local_embeddings(),
    cache_path=cache_path,
    namespace=DEFAULT_EMBEDDING_MODEL,
)

start = time.perf_counter()
first_vectors = cached_embeddings.embed_documents(texts)
first_elapsed = time.perf_counter() - start

start = time.perf_counter()
second_vectors = cached_embeddings.embed_documents(texts)
second_elapsed = time.perf_counter() - start

print(f"documents={len(texts)}")
print(f"first_call_seconds={first_elapsed:.3f}")
print(f"second_call_seconds={second_elapsed:.3f}")
print(f"vector_dimension={len(first_vectors[0])}")
print(f"same_dimension={len(first_vectors[0]) == len(second_vectors[0])}")
print(cache_path)
