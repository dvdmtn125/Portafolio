from dataclasses import dataclass, field
from typing import List


@dataclass
class Quote:
    text: str
    author: str
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "author": self.author,
            "tags": self.tags,
        }