from dataclasses import dataclass, field
from typing import Any


@dataclass
class EligibilityError:
    code: str
    params: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            code=data["code"],
            params=data.get("params", {}),
        )