from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class FareOption:
    airline: str
    booking_class: str
    base_fare: float
    taxes: float
    contract_code: str | None = None
    fare_type: str = "public"
    refundable: bool = False
    baggage_included: bool = False

    @property
    def total_price(self) -> float:
        return round(self.base_fare + self.taxes, 2)

    @property
    def is_private_net_fare(self) -> bool:
        fare_type = self.fare_type.lower()
        return fare_type in {"private", "net", "private_net", "private net"}


def normalize_booking_class(booking_class: str) -> str:
    booking = booking_class.strip().upper()
    if not booking:
        raise ValueError("booking_class cannot be empty")
    return booking


def fare_score(fare: FareOption) -> float:
    score = 0.0

    score -= fare.total_price

    if fare.is_private_net_fare:
        score += 75

    if fare.contract_code:
        score += 30

    if fare.refundable:
        score += 20

    if fare.baggage_included:
        score += 10

    premium_booking_classes = {"J", "C", "D", "Z", "P", "F", "A"}
    if normalize_booking_class(fare.booking_class) in premium_booking_classes:
        score += 8

    return round(score, 2)


def optimize_fare_options(fares: Iterable[FareOption]) -> List[dict]:
    optimized = []
    for fare in fares:
        optimized.append(
            {
                "airline": fare.airline,
                "booking_class": normalize_booking_class(fare.booking_class),
                "contract_code": fare.contract_code or "N/A",
                "fare_type": fare.fare_type,
                "is_private_net_fare": fare.is_private_net_fare,
                "total_price": fare.total_price,
                "score": fare_score(fare),
            }
        )

    return sorted(optimized, key=lambda item: item["score"], reverse=True)

