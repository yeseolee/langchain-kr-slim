from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.document_utils import load_directory_documents

data_dir = Path(__file__).resolve().parent / "data"
documents = load_directory_documents(data_dir)

print(f"documents={len(documents)}")
for document in documents[:5]:
    print(document.metadata)
