from dataclasses import dataclass, field


@dataclass
class Discount:
    id: int
    name: str
    active: bool
    card_types: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            name=data["name"],
            active=data.get("active", False),
            card_types=data.get("cardTypes", []),
        )


@dataclass
class Partner:
    name: str
    amount_paid_reporting: bool
    language_code: str
    currency: str
    discounts: list[Discount] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data["name"],
            amount_paid_reporting=data.get("amountPaidReporting", False),
            language_code=data.get("languageCode", ""),
            currency=data.get("currency", ""),
            discounts=[
                Discount.from_dict(discount)
                for discount in data.get("discounts", [])
            ],
        )