from typing import List, Dict, Optional

from app.repositories.json_repository import JsonRepository


class BusinessRepository(JsonRepository):
    def __init__(self):
        super().__init__("businesses.json")

    def find_by_id(self, business_id: int) -> Optional[Dict]:
        businesses = self.find_all()
        return next((b for b in businesses if b.get("id") == business_id), None)
