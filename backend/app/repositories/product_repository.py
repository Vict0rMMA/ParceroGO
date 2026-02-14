from typing import List, Dict, Optional

from app.repositories.json_repository import JsonRepository


class ProductRepository(JsonRepository):
    def __init__(self):
        super().__init__("products.json")

    def find_by_id(self, product_id: int) -> Optional[Dict]:
        products = self.find_all()
        return next((p for p in products if p.get("id") == product_id), None)

    def find_by_business_id(self, business_id: int, only_available: bool = True) -> List[Dict]:
        products = self.find_all()
        out = [p for p in products if p.get("business_id") == business_id]
        if only_available:
            out = [p for p in out if p.get("available", True)]
        return out
