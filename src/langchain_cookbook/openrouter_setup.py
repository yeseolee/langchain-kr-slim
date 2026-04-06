from __future__ import annotations

import asyncio
import os
import time
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, AsyncIterator, Awaitable, Callable, Iterator, TypeVar

import openai
from dotenv import dotenv_values
from langchain_openai import ChatOpenAI

API_KEY_PLACEHOLDER = "YOUR_OPENROUTER_API_KEY_HERE"
DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "openai/gpt-oss-20b:free"
DEFAULT_TEMPERATURE = 0.2
DEFAULT_TIMEOUT = (10.0, 60.0)
CLIENT_MAX_RETRIES = 0
MODEL_RETRY_ATTEMPTS = 6
RETRY_BASE_DELAY_SECONDS = 2.0
RETRY_MAX_DELAY_SECONDS = 20.0

T = TypeVar("T")


@dataclass(frozen=True)
class OpenRouterSettings:
    base_url: str
    api_key: str
    model: str


def _is_retryable_error(error: Exception) -> bool:
    if isinstance(
        error,
        (
            openai.RateLimitError,
            openai.APIConnectionError,
            openai.APITimeoutError,
            openai.InternalServerError,
        ),
    ):
        return True
    if isinstance(error, openai.APIStatusError):
        return error.status_code in {429, 500, 502, 503, 504}
    return False


def _retry_delay_seconds(error: Exception, attempt: int) -> float:
    response = getattr(error, "response", None)
    headers = getattr(response, "headers", None)
    if headers is not None:
        retry_after = headers.get("retry-after") or headers.get("Retry-After")
        if retry_after:
            try:
                return max(float(retry_after), 0.0)
            except ValueError:
                pass
    return min(RETRY_BASE_DELAY_SECONDS * (2 ** (attempt - 1)), RETRY_MAX_DELAY_SECONDS)


class ResilientChatOpenAI(ChatOpenAI):
    def _with_retry(self, operation: Callable[[], T]) -> T:
        for attempt in range(1, MODEL_RETRY_ATTEMPTS + 1):
            try:
                return operation()
            except Exception as error:
                if not _is_retryable_error(error) or attempt == MODEL_RETRY_ATTEMPTS:
                    raise
                time.sleep(_retry_delay_seconds(error, attempt))
        raise RuntimeError("unreachable")

    async def _with_retry_async(self, operation: Callable[[], Awaitable[T]]) -> T:
        for attempt in range(1, MODEL_RETRY_ATTEMPTS + 1):
            try:
                return await operation()
            except Exception as error:
                if not _is_retryable_error(error) or attempt == MODEL_RETRY_ATTEMPTS:
                    raise
                await asyncio.sleep(_retry_delay_seconds(error, attempt))
        raise RuntimeError("unreachable")

    def _generate(
        self,
        messages: list[Any],
        stop: list[str] | None = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> Any:
        return self._with_retry(
            lambda: super(ResilientChatOpenAI, self)._generate(
                messages,
                stop=stop,
                run_manager=run_manager,
                **kwargs,
            )
        )

    def _stream(
        self,
        messages: list[Any],
        stop: list[str] | None = None,
        run_manager: Any = None,
        *,
        stream_usage: bool | None = None,
        **kwargs: Any,
    ) -> Iterator[Any]:
        attempt = 1
        while True:
            yielded_any = False
            try:
                for chunk in super(ResilientChatOpenAI, self)._stream(
                    messages,
                    stop=stop,
                    run_manager=run_manager,
                    stream_usage=stream_usage,
                    **kwargs,
                ):
                    yielded_any = True
                    yield chunk
                return
            except Exception as error:
                if yielded_any or not _is_retryable_error(error) or attempt == MODEL_RETRY_ATTEMPTS:
                    raise
                time.sleep(_retry_delay_seconds(error, attempt))
                attempt += 1

    async def _agenerate(
        self,
        messages: list[Any],
        stop: list[str] | None = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> Any:
        return await self._with_retry_async(
            lambda: super(ResilientChatOpenAI, self)._agenerate(
                messages,
                stop=stop,
                run_manager=run_manager,
                **kwargs,
            )
        )

    async def _astream(
        self,
        messages: list[Any],
        stop: list[str] | None = None,
        run_manager: Any = None,
        *,
        stream_usage: bool | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[Any]:
        attempt = 1
        while True:
            yielded_any = False
            try:
                async for chunk in super(ResilientChatOpenAI, self)._astream(
                    messages,
                    stop=stop,
                    run_manager=run_manager,
                    stream_usage=stream_usage,
                    **kwargs,
                ):
                    yielded_any = True
                    yield chunk
                return
            except Exception as error:
                if yielded_any or not _is_retryable_error(error) or attempt == MODEL_RETRY_ATTEMPTS:
                    raise
                await asyncio.sleep(_retry_delay_seconds(error, attempt))
                attempt += 1


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
) -> ResilientChatOpenAI:
    settings = load_openrouter_settings()
    return ResilientChatOpenAI(
        model=settings.model,
        base_url=settings.base_url,
        api_key=settings.api_key,
        temperature=temperature,
        timeout=timeout or DEFAULT_TIMEOUT,
        max_retries=CLIENT_MAX_RETRIES,
        max_completion_tokens=max_completion_tokens,
    )
