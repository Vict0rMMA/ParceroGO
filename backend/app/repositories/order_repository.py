from typing import List, Dict, Optional

from app.repositories.json_repository import JsonRepository


class OrderRepository(JsonRepository):
    def __init__(self):
        super().__init__("orders.json")

    def find_by_id(self, order_id: int) -> Optional[Dict]:
        orders = self.find_all()
        return next((o for o in orders if o.get("id") == order_id), None)

    def find_by_phone_normalized(self, normalized_phone: str) -> List[Dict]:
        orders = self.find_all()
        return [
            o for o in orders
            if self._normalize_phone(o.get("customer_phone", "")) == normalized_phone
        ]

    @staticmethod
    def _normalize_phone(phone: str) -> str:
        s = "".join(c for c in str(phone or "") if c.isdigit())
        return s[2:] if len(s) == 12 and s.startswith("57") else s

    def append_and_save(self, order: Dict) -> None:
        orders = self.find_all()
        orders.append(order)
        self.save_all(orders)

    def update_and_save(self, order: Dict) -> None:
        orders = self.find_all()
        for i, o in enumerate(orders):
            if o.get("id") == order.get("id"):
                orders[i] = order
                break
        self.save_all(orders)
