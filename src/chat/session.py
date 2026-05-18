"""Session memory, persistence, and demo-level rate limiting."""

from __future__ import annotations

import json
import re
from collections import deque
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class ChatTurn:
    role: str
    content: str
    created_at: str
    metadata: dict[str, Any] | None = None


def new_session_id() -> str:
    return uuid4().hex[:12]


def slugify_user_name(user_name: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "-", user_name.strip().lower())
    return cleaned.strip("-") or "anonymous"


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


def append_turn(
    history: list[ChatTurn],
    *,
    role: str,
    content: str,
    metadata: dict[str, Any] | None = None,
) -> list[ChatTurn]:
    return [
        *history,
        ChatTurn(role=role, content=content, created_at=now_iso(), metadata=metadata),
    ]


def recent_history_lines(history: list[ChatTurn], *, max_turns: int = 6) -> list[str]:
    recent = history[-max_turns:]
    return [f"{turn.role}: {turn.content}" for turn in recent]


def conversation_dir(base_path: Path, user_name: str) -> Path:
    return base_path / slugify_user_name(user_name)


def conversation_path(base_path: Path, user_name: str, session_id: str) -> Path:
    return conversation_dir(base_path, user_name) / f"{session_id}.json"


def save_conversation(
    *,
    base_path: Path,
    user_name: str,
    session_id: str,
    history: list[ChatTurn],
) -> Path:
    path = conversation_path(base_path, user_name, session_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "user_name": user_name,
        "session_id": session_id,
        "updated_at": now_iso(),
        "history": [asdict(turn) for turn in history],
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def load_conversation(*, base_path: Path, user_name: str, session_id: str) -> list[ChatTurn]:
    path = conversation_path(base_path, user_name, session_id)
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    history = payload.get("history", [])
    return [ChatTurn(**turn) for turn in history]


def list_conversations(*, base_path: Path, user_name: str) -> list[dict[str, str]]:
    directory = conversation_dir(base_path, user_name)
    if not directory.exists():
        return []

    conversations: list[dict[str, str]] = []
    for path in sorted(directory.glob("*.json"), reverse=True):
        payload = json.loads(path.read_text(encoding="utf-8"))
        history = payload.get("history", [])
        preview = ""
        for turn in reversed(history):
            if turn.get("role") == "user":
                preview = str(turn.get("content", ""))[:80]
                break
        conversations.append(
            {
                "session_id": str(payload.get("session_id", path.stem)),
                "updated_at": str(payload.get("updated_at", "")),
                "preview": preview or "Conversation without user prompt",
            }
        )
    return conversations


class SlidingWindowRateLimiter:
    """Simple in-memory rate limiter for demo sessions."""

    def __init__(self, *, max_calls: int, window_seconds: int) -> None:
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self._timestamps: deque[float] = deque()

    def allow(self, *, now_ts: float) -> tuple[bool, int]:
        boundary = now_ts - self.window_seconds
        while self._timestamps and self._timestamps[0] <= boundary:
            self._timestamps.popleft()
        if len(self._timestamps) >= self.max_calls:
            retry_after = max(1, int(self.window_seconds - (now_ts - self._timestamps[0])))
            return False, retry_after
        self._timestamps.append(now_ts)
        return True, 0
