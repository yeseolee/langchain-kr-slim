from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.document_utils import load_json_documents

data_path = Path(__file__).resolve().parent / "data" / "people.json"
documents = load_json_documents(data_path)

print(f"documents={len(documents)}")
print(documents[0].metadata)
print(documents[0].page_content)
