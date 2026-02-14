from typing import List, Dict, Any

from app.utils import load_json, save_json


class JsonRepository:
    def __init__(self, file_name: str):
        self._file_name = file_name

    def find_all(self) -> List[Dict[str, Any]]:
        data = load_json(self._file_name)
        return data if isinstance(data, list) else []

    def save_all(self, data: List[Dict[str, Any]]) -> None:
        save_json(self._file_name, data)
