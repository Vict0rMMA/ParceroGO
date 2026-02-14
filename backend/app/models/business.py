from dataclasses import dataclass
from typing import Optional


@dataclass
class Business:
    id: int
    name: str
    category: str
    address: str
    latitude: float
    longitude: float
    phone: str
    rating: float = 0.0
    is_open: bool = True
    delivery_time: int = 30

    @classmethod
    def from_dict(cls, d: dict) -> "Business":
        return cls(
            id=d["id"],
            name=d["name"],
            category=d["category"],
            address=d["address"],
            latitude=d["latitude"],
            longitude=d["longitude"],
            phone=d["phone"],
            rating=d.get("rating", 0.0),
            is_open=d.get("is_open", True),
            delivery_time=d.get("delivery_time", 30),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "phone": self.phone,
            "rating": self.rating,
            "is_open": self.is_open,
            "delivery_time": self.delivery_time,
        }
