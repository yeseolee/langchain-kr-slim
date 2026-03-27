from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import requests
from dotenv import dotenv_values
from langchain_core.embeddings import Embeddings
from langchain_openai import ChatOpenAI

API_KEY_PLACEHOLDER = "YOUR_OPENROUTER_API_KEY_HERE"
SMALL_MODEL_TEMPERATURE = 0.3
LARGE_MODEL_TEMPERATURE = 0.1
MAX_RETRIES = 3
EMBED_TIKTOKEN_ENABLED = False
CHECK_EMBEDDING_CTX_LENGTH = False


@dataclass(frozen=True)
class OpenRouterSettings:
    base_url: str
    api_key: str
    small_model: str
    large_model: str
    embedding_model: str
    site_url: str
    app_name: str


class OpenRouterEmbeddings(Embeddings):
    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        model: str,
        timeout: int = 60,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    def _post_embeddings(self, input_value: str | list[str]) -> list[list[float]]:
        response = requests.post(
            f"{self.base_url}/embeddings",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "input": input_value,
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload = response.json()
        data = payload.get("data", [])
        if not data:
            raise ValueError(f"No embedding data received: {payload}")
        return [item["embedding"] for item in data]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._post_embeddings(texts)

    def embed_query(self, text: str) -> list[float]:
        return self._post_embeddings(text)[0]


def _iter_search_roots() -> list[Path]:
    seen: set[Path] = set()
    roots: list[Path] = []

    for base in [Path.cwd(), Path(__file__).resolve().parent]:
        for candidate in [base, *base.parents]:
            resolved = candidate.resolve()
            if resolved not in seen:
                seen.add(resolved)
                roots.append(resolved)

    return roots


def find_project_file(filename: str) -> Path | None:
    for root in _iter_search_roots():
        candidate = root / filename
        if candidate.exists():
            return candidate
    return None


def _load_env_values() -> dict[str, str]:
    merged: dict[str, str] = {}

    env_example_file = find_project_file(".env-example")
    if env_example_file is not None:
        merged.update(
            {
                key: value
                for key, value in dotenv_values(env_example_file).items()
                if value is not None
            }
        )

    env_file = find_project_file(".env")
    if env_file is not None:
        merged.update(
            {
                key: value
                for key, value in dotenv_values(env_file).items()
                if value is not None
            }
        )

    merged.update(os.environ)
    return {
        key: value.strip() if isinstance(value, str) else value
        for key, value in merged.items()
    }


def _read_required_env(env_values: dict[str, str], name: str) -> str:
    value = env_values.get(name, "").strip()
    if not value:
        raise ValueError(
            "프로젝트 루트의 .env-example 또는 .env 파일에서 "
            f"{name} 값을 먼저 설정하세요."
        )
    return value


@lru_cache(maxsize=1)
def load_openrouter_settings() -> OpenRouterSettings:
    env_values = _load_env_values()

    api_key = _read_required_env(env_values, "OPENROUTER_API_KEY")
    if api_key == API_KEY_PLACEHOLDER:
        raise ValueError(
            "프로젝트 루트의 .env-example 또는 .env 파일에서 "
            "OPENROUTER_API_KEY 값을 먼저 설정하세요."
        )

    os.environ["OPENROUTER_API_KEY"] = api_key

    return OpenRouterSettings(
        base_url=_read_required_env(env_values, "OPENROUTER_BASE_URL"),
        api_key=api_key,
        small_model=_read_required_env(env_values, "OPENROUTER_SMALL_MODEL"),
        large_model=_read_required_env(env_values, "OPENROUTER_LARGE_MODEL"),
        embedding_model=_read_required_env(env_values, "OPENROUTER_EMBED_MODEL"),
        site_url=env_values.get("OPENROUTER_SITE_URL", ""),
        app_name=env_values.get("OPENROUTER_APP_NAME", ""),
    )


def make_chat_model(model_name: str, temperature: float) -> ChatOpenAI:
    settings = load_openrouter_settings()
    return ChatOpenAI(
        model=model_name,
        base_url=settings.base_url,
        api_key=settings.api_key,
        temperature=temperature,
        max_retries=MAX_RETRIES,
    )


def make_small_chat_model() -> ChatOpenAI:
    settings = load_openrouter_settings()
    return make_chat_model(settings.small_model, SMALL_MODEL_TEMPERATURE)


def make_large_chat_model() -> ChatOpenAI:
    settings = load_openrouter_settings()
    return make_chat_model(settings.large_model, LARGE_MODEL_TEMPERATURE)


def make_embeddings(model_name: str | None = None) -> OpenRouterEmbeddings:
    settings = load_openrouter_settings()
    resolved_model = model_name or settings.embedding_model
    return OpenRouterEmbeddings(
        model=resolved_model,
        base_url=settings.base_url,
        api_key=settings.api_key,
    )
