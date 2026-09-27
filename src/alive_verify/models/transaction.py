from dataclasses import dataclass
from datetime import datetime

from ..utils import parse_datetime


@dataclass
class Transaction:
    id: int
    created_on: datetime
    discount_id: int
    verification_id: int
    amount_paid: float
    issued_on: datetime

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            created_on=parse_datetime(data["createdOn"]),
            discount_id=data["discountId"],
            verification_id=data["verificationId"],
            amount_paid=data["amountPaid"],
            issued_on=parse_datetime(data["issuedOn"]),
        )