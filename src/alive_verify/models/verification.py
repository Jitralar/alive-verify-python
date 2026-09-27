from dataclasses import dataclass, field
from .eligibility import EligibilityError

from datetime import date, datetime
from ..utils import parse_date, parse_datetime

from ..enums import (
    CardType,
    FailureReason,
    VerificationMode,
    VerificationResult,
)

@dataclass
class Verification:
    id: int
    created_on: datetime
    mode: VerificationMode
    result: VerificationResult

    card_number: str | None = None
    cardholder_name: str | None = None
    cardholder_date_of_birth: date | None = None
    discount_id: int | None = None
    reason: FailureReason | None = None
    card_type: CardType | None = None
    chip_number: str | None = None
    cardholder_phone: str | None = None
    card_valid_longer_than: date | None = None
    eligibility_errors: list[EligibilityError] = field(default_factory=list)
    @property
    def successful(self) -> bool:
        return self.result == VerificationResult.SUCCESSFUL

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            created_on=parse_datetime(data["createdOn"]),
            mode=VerificationMode(data["mode"]),
            result=VerificationResult(data["result"]),
            card_number=data.get("cardNumber"),
            cardholder_name=data.get("cardholderName"),
            cardholder_date_of_birth=(
                parse_date(data["cardholderDateOfBirth"])
                if data.get("cardholderDateOfBirth")
                else None
            ),
            discount_id=data.get("discountId"),
            reason=(
                FailureReason(data["reason"])
                if data.get("reason")
                else None
            ),
            card_type=(
                CardType(data["cardType"])
                if data.get("cardType")
                else None
            ),
            chip_number=data.get("chipNumber"),
            cardholder_phone=data.get("cardholderPhone"),
            card_valid_longer_than=(
                parse_date(data["cardValidLongerThan"])
                if data.get("cardValidLongerThan")
                else None
            ),
            eligibility_errors=[
                EligibilityError.from_dict(error)
                for error in data.get("eligibilityErrors", [])
            ],
        )