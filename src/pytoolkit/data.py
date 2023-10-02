"""Data Module."""
from dataclasses import dataclass, field

sample_headers = {'test': 1}
@dataclass
class Response:
    body: str
    status: int = field(default=200)
    headers: dict = field(default_factory=dict)
    def __init__(self, body:str, status: int=200):
        self.body = body
        self.status = status
        self.headers = sample_headers
