from __future__ import annotations

import json
import os
import pickle
import sys
from pathlib import Path

from langchain_core.load import dumpd, dumps, load, loads
from langchain_core.prompts import PromptTemplate

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model
from langchain_cookbook.openrouter_setup import load_openrouter_settings

artifacts_dir = Path(__file__).resolve().parent / "artifacts"
artifacts_dir.mkdir(exist_ok=True)

settings = load_openrouter_settings()
os.environ["OPENAI_API_KEY"] = settings.api_key

prompt = PromptTemplate.from_template("{fruit}의 색상이 무엇입니까?")
chain = prompt | make_chat_model(temperature=0)

print(f"Chat model serializable: {chain.is_lc_serializable()}")

serialized_dict = dumpd(chain)
serialized_text = dumps(chain)

pickle_path = artifacts_dir / "fruit_chain.pkl"
json_path = artifacts_dir / "fruit_chain.json"

with pickle_path.open("wb") as file:
    pickle.dump(serialized_dict, file)

with json_path.open("w", encoding="utf-8") as file:
    json.dump(serialized_dict, file, ensure_ascii=False, indent=2)

with pickle_path.open("rb") as file:
    loaded_dict = pickle.load(file)

chain_from_dict = load(
    loaded_dict,
    allowed_objects="all",
    secrets_map={"OPENAI_API_KEY": settings.api_key},
)
chain_from_text = loads(serialized_text, allowed_objects="all")

print(type(serialized_dict).__name__)
print(type(serialized_text).__name__)
print(type(chain_from_dict).__name__)
print(type(chain_from_text).__name__)
