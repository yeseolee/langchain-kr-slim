from __future__ import annotations

import sys
from pathlib import Path

from langchain_text_splitters import CharacterTextSplitter, TokenTextSplitter
from transformers import AutoTokenizer

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


data_path = Path(__file__).resolve().parent / "data" / "appendix-keywords.txt"
text = data_path.read_text(encoding="utf-8")

tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
character_splitter = CharacterTextSplitter.from_huggingface_tokenizer(
    tokenizer=tokenizer,
    chunk_size=140,
    chunk_overlap=20,
)
token_splitter = TokenTextSplitter(chunk_size=80, chunk_overlap=10)

character_chunks = character_splitter.split_text(text)
token_chunks = token_splitter.split_text(text)

print("character_chunks", len(character_chunks))
print(character_chunks[0][:220])
print("=" * 30)
print("token_chunks", len(token_chunks))
print(token_chunks[0][:220])
