from __future__ import annotations

import sys
import time
from pathlib import Path

from langchain_core.caches import InMemoryCache
from langchain_core.globals import get_llm_cache, set_llm_cache
from langchain_core.prompts import PromptTemplate

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from langchain_cookbook.example_utils import make_chat_model

prompt = PromptTemplate.from_template("{country}에 대해서 200자 내외로 요약해줘")
chain = prompt | make_chat_model(temperature=0)

start = time.perf_counter()
first_response = chain.invoke({"country": "한국"})
first_elapsed = time.perf_counter() - start

set_llm_cache(InMemoryCache())

start = time.perf_counter()
cached_response = chain.invoke({"country": "한국"})
second_elapsed = time.perf_counter() - start

start = time.perf_counter()
cached_response_again = chain.invoke({"country": "한국"})
third_elapsed = time.perf_counter() - start

print("[first_call_seconds]")
print(round(first_elapsed, 3))
print(first_response.content)
print()

print("[cache_enabled]")
print(type(get_llm_cache()).__name__)
print()

print("[second_call_seconds]")
print(round(second_elapsed, 3))
print(cached_response.content)
print()

print("[third_call_seconds]")
print(round(third_elapsed, 3))
print(cached_response_again.content)
