from dataclasses import dataclass
from typing import Optional


@dataclass
class Courier:
    id: int
    name: str
    phone: str
    lat: float
    lng: float
    zone: str = ""
    available: bool = True
    vehicle: str = ""
    rating: float = 0.0
    current_order_id: Optional[int] = None
    total_deliveries: int = 0

    @classmethod
    def from_dict(cls, d: dict) -> "Courier":
        return cls(
            id=d["id"],
            name=d["name"],
            phone=d["phone"],
            lat=d["lat"],
            lng=d["lng"],
            zone=d.get("zone", ""),
            available=d.get("available", True),
            vehicle=d.get("vehicle", ""),
            rating=d.get("rating", 0.0),
            current_order_id=d.get("current_order_id"),
            total_deliveries=d.get("total_deliveries", 0),
        )

    def to_dict(self) -> dict:
        d = {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "lat": self.lat,
            "lng": self.lng,
            "zone": self.zone,
            "available": self.available,
            "vehicle": self.vehicle,
            "rating": self.rating,
            "total_deliveries": self.total_deliveries,
        }
        if self.current_order_id is not None:
            d["current_order_id"] = self.current_order_id
        return d
