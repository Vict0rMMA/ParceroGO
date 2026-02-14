from typing import List, Dict, Optional

from app.repositories.json_repository import JsonRepository


class PaymentRepository(JsonRepository):
    def __init__(self):
        super().__init__("payments.json")

    def find_by_order_id(self, order_id: int) -> Optional[Dict]:
        payments = self.find_all()
        return next((p for p in payments if p.get("order_id") == order_id), None)

    def append_and_save(self, payment: Dict) -> None:
        payments = self.find_all()
        payments.append(payment)
        self.save_all(payments)
