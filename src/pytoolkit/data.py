"""Data Module."""

from typing import Any
from dataclasses import dataclass, field


sample_headers: dict[str, int] = {"test": 1}


@dataclass
class Response:
    """Mock Response."""

    body: str
    status: int = field(default=200)
    headers: dict[Any, Any] = field(default_factory=dict)

    def __init__(self, body: str, status: int = 200):
        self.body = body
        self.status = status
        self.headers = sample_headers
