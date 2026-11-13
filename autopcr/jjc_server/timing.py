"""Correlated, monotonic stage timings for JJC recommendation requests."""

from __future__ import annotations

import secrets
import time
from contextlib import contextmanager
from contextvars import ContextVar
from functools import wraps
from typing import Any, Awaitable, Callable, Iterator

from ..util.logger import instance as logging


_trace_id: ContextVar[str | None] = ContextVar("jjc_suggestion_trace_id", default=None)
_mode: ContextVar[str | None] = ContextVar("jjc_suggestion_mode", default=None)


def current_trace_id() -> str | None:
    return _trace_id.get()


@contextmanager
def suggestion_trace(mode: str) -> Iterator[str]:
    existing = _trace_id.get()
    if existing is not None:
        yield existing
        return
    trace_token = _trace_id.set(secrets.token_hex(8))
    mode_token = _mode.set(mode)
    try:
        yield _trace_id.get() or "-"
    finally:
        _mode.reset(mode_token)
        _trace_id.reset(trace_token)


def log_stage(stage: str, started: float, **details: object) -> None:
    fields = " ".join(f"{key}={value}" for key, value in details.items())
    logging.info(
        "[JJC-PERF] trace=%s mode=%s stage=%s elapsed_ms=%.1f%s",
        _trace_id.get() or "-",
        _mode.get() or "-",
        stage,
        (time.perf_counter() - started) * 1000,
        f" {fields}" if fields else "",
    )


def timed_suggestion(mode: str, stage: str) -> Callable[[Callable[..., Awaitable[Any]]], Callable[..., Awaitable[Any]]]:
    """Log total time even when a suggestion stage raises or is cancelled."""
    def decorate(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        @wraps(func)
        async def wrapped(*args: Any, **kwargs: Any) -> Any:
            with suggestion_trace(mode):
                started = time.perf_counter()
                try:
                    return await func(*args, **kwargs)
                finally:
                    log_stage(stage, started)
        return wrapped
    return decorate
