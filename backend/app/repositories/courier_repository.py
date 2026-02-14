from typing import List, Dict, Optional

from app.repositories.json_repository import JsonRepository


class CourierRepository(JsonRepository):
    def __init__(self):
        super().__init__("couriers.json")

    def find_by_id(self, courier_id: int) -> Optional[Dict]:
        couriers = self.find_all()
        return next((c for c in couriers if c.get("id") == courier_id), None)

    def find_available(self) -> List[Dict]:
        couriers = self.find_all()
        return [c for c in couriers if c.get("available", True)]

    def update_and_save(self, courier: Dict) -> None:
        couriers = self.find_all()
        for i, c in enumerate(couriers):
            if c.get("id") == courier.get("id"):
                couriers[i] = courier
                break
        self.save_all(couriers)
