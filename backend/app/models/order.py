from dataclasses import dataclass, field
from typing import List, Optional, Any
from datetime import datetime


@dataclass
class OrderProduct:
    product_id: int
    product_name: str
    quantity: int
    unit_price: float
    subtotal: float
    notes: str = ""

    @classmethod
    def from_dict(cls, d: dict) -> "OrderProduct":
        return cls(
            product_id=d["product_id"],
            product_name=d["product_name"],
            quantity=d["quantity"],
            unit_price=d["unit_price"],
            subtotal=d["subtotal"],
            notes=d.get("notes") or "",
        )

    def to_dict(self) -> dict:
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "subtotal": self.subtotal,
            "notes": self.notes,
        }


@dataclass
class Order:
    id: int
    customer_name: str
    customer_phone: str
    customer_address: str
    customer_lat: float
    customer_lng: float
    business_id: int
    business_name: str
    business_lat: float
    business_lng: float
    products: List[OrderProduct]
    total: float
    distance_km: float
    estimated_time: int
    payment_method: str
    tip_amount: int
    payment_status: str
    status: str
    delivery_person: Optional[str] = None
    courier_phone: Optional[str] = None
    courier_id: Optional[int] = None
    courier_name: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    status_history: List[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        d = {
            "id": self.id,
            "customer_name": self.customer_name,
            "customer_phone": self.customer_phone,
            "customer_address": self.customer_address,
            "customer_lat": self.customer_lat,
            "customer_lng": self.customer_lng,
            "business_id": self.business_id,
            "business_name": self.business_name,
            "business_lat": self.business_lat,
            "business_lng": self.business_lng,
            "products": [p.to_dict() for p in self.products],
            "total": self.total,
            "distance_km": self.distance_km,
            "estimated_time": self.estimated_time,
            "payment_method": self.payment_method,
            "tip_amount": self.tip_amount,
            "payment_status": self.payment_status,
            "status": self.status,
            "delivery_person": self.delivery_person,
            "courier_phone": self.courier_phone,
            "created_at": self.created_at,
            "status_history": self.status_history,
        }
        if self.courier_id is not None:
            d["courier_id"] = self.courier_id
        if self.courier_name is not None:
            d["courier_name"] = self.courier_name
        if self.updated_at is not None:
            d["updated_at"] = self.updated_at
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Order":
        products = [OrderProduct.from_dict(p) for p in d.get("products", [])]
        return cls(
            id=d["id"],
            customer_name=d["customer_name"],
            customer_phone=d["customer_phone"],
            customer_address=d["customer_address"],
            customer_lat=d["customer_lat"],
            customer_lng=d["customer_lng"],
            business_id=d["business_id"],
            business_name=d["business_name"],
            business_lat=d["business_lat"],
            business_lng=d["business_lng"],
            products=products,
            total=d["total"],
            distance_km=d["distance_km"],
            estimated_time=d["estimated_time"],
            payment_method=d.get("payment_method", "efectivo"),
            tip_amount=d.get("tip_amount", 0),
            payment_status=d.get("payment_status", "pendiente"),
            status=d["status"],
            delivery_person=d.get("delivery_person"),
            courier_phone=d.get("courier_phone"),
            courier_id=d.get("courier_id"),
            courier_name=d.get("courier_name"),
            created_at=d.get("created_at"),
            updated_at=d.get("updated_at"),
            status_history=d.get("status_history") or [],
        )
