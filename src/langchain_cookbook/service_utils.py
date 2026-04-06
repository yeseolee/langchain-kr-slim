from __future__ import annotations

import os


def require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ValueError(f"{name} 환경 변수를 먼저 설정하세요.")
    return value


def get_env(name: str, default: str) -> str:
    value = os.getenv(name, "").strip()
    return value or default


__all__ = ["get_env", "require_env"]
