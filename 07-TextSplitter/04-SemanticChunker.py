from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_local_embeddings
from langchain_cookbook.semantic_utils import semantic_chunk_text


data_path = Path(__file__).resolve().parent / "data" / "appendix-keywords.txt"
text = data_path.read_text(encoding="utf-8")

chunks = semantic_chunk_text(text, embeddings=make_local_embeddings(), max_sentences_per_chunk=3)
for index, chunk in enumerate(chunks[:5], start=1):
    print(f"chunk {index}")
    print(chunk[:300])
    print("=" * 30)
