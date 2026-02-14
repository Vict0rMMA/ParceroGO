from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    id: int
    business_id: int
    name: str
    price: float
    description: str = ""
    category: str = ""
    available: bool = True
    image: str = ""

    @classmethod
    def from_dict(cls, d: dict) -> "Product":
        return cls(
            id=d["id"],
            business_id=d["business_id"],
            name=d["name"],
            price=d["price"],
            description=d.get("description", ""),
            category=d.get("category", ""),
            available=d.get("available", True),
            image=d.get("image", ""),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "business_id": self.business_id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "category": self.category,
            "available": self.available,
            "image": self.image,
        }
