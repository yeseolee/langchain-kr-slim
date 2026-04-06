from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path
from typing import Sequence

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict


def last_k_turn_messages(messages: Sequence[BaseMessage], k: int) -> list[BaseMessage]:
    return list(messages[-(2 * k) :])


def _normalize_table_name(table_name: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9_]", "_", table_name)
    return normalized or "chat_history"


class SQLiteChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, *, session_id: str, db_path: str | Path, table_name: str) -> None:
        self.session_id = session_id
        self.db_path = str(Path(db_path))
        self.table_name = _normalize_table_name(table_name)
        self._ensure_table()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _ensure_table(self) -> None:
        with self._connect() as conn:
            conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    payload TEXT NOT NULL
                )
                """
            )

    @property
    def messages(self) -> list[BaseMessage]:
        with self._connect() as conn:
            rows = conn.execute(
                f"""
                SELECT payload
                FROM {self.table_name}
                WHERE session_id = ?
                ORDER BY id
                """,
                (self.session_id,),
            ).fetchall()
        payloads = [json.loads(payload) for (payload,) in rows]
        return messages_from_dict(payloads)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        rows = [
            (self.session_id, json.dumps(message_to_dict(message), ensure_ascii=False))
            for message in messages
        ]
        with self._connect() as conn:
            conn.executemany(
                f"INSERT INTO {self.table_name} (session_id, payload) VALUES (?, ?)",
                rows,
            )

    def clear(self) -> None:
        with self._connect() as conn:
            conn.execute(
                f"DELETE FROM {self.table_name} WHERE session_id = ?",
                (self.session_id,),
            )


__all__ = ["SQLiteChatMessageHistory", "last_k_turn_messages"]
