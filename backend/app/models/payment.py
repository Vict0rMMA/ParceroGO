from dataclasses import dataclass


@dataclass
class Payment:
    id: int
    order_id: int
    amount: float
    tip_amount: float
    payment_method: str
    status: str
    created_at: str

    @classmethod
    def from_dict(cls, d: dict) -> "Payment":
        return cls(
            id=d["id"],
            order_id=d["order_id"],
            amount=d["amount"],
            tip_amount=d.get("tip_amount", 0),
            payment_method=d.get("payment_method", "efectivo"),
            status=d["status"],
            created_at=d["created_at"],
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "order_id": self.order_id,
            "amount": self.amount,
            "tip_amount": self.tip_amount,
            "payment_method": self.payment_method,
            "status": self.status,
            "created_at": self.created_at,
        }
