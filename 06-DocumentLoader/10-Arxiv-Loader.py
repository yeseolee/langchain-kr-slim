from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.document_utils import load_arxiv_documents


try:
    documents = load_arxiv_documents("chain of thought", load_max_docs=2)
except Exception as exc:
    print(f"arxiv request failed: {exc}")
else:
    for document in documents:
        print(json.dumps(document.metadata, ensure_ascii=False, indent=2))
        print(document.page_content[:300])
        print("=" * 30)
