from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import dotenv_values
from langchain_openai import ChatOpenAI

API_KEY_PLACEHOLDER = "YOUR_OPENROUTER_API_KEY_HERE"
DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "openai/gpt-oss-20b:free"
DEFAULT_TEMPERATURE = 0.2
MAX_RETRIES = 3


@dataclass(frozen=True)
class OpenRouterSettings:
    base_url: str
    api_key: str
    model: str


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
        base_url=env_values.get("OPENROUTER_BASE_URL", DEFAULT_BASE_URL),
        api_key=api_key,
        model=env_values.get("OPENROUTER_MODEL", DEFAULT_MODEL),
    )


def make_chat_model(
    temperature: float = DEFAULT_TEMPERATURE,
    *,
    timeout: float | tuple[float, float] | None = None,
    max_completion_tokens: int | None = None,
) -> ChatOpenAI:
    settings = load_openrouter_settings()
    return ChatOpenAI(
        model=settings.model,
        base_url=settings.base_url,
        api_key=settings.api_key,
        temperature=temperature,
        timeout=timeout,
        max_retries=MAX_RETRIES,
        max_completion_tokens=max_completion_tokens,
    )
