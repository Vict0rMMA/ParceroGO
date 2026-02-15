from typing import Dict, Optional

from app.repositories.order_repository import OrderRepository
from app.repositories.courier_repository import CourierRepository
from app.services.geo_service import GeoService


class CourierService:
    def __init__(
        self,
        order_repo: Optional[OrderRepository] = None,
        courier_repo: Optional[CourierRepository] = None,
        geo: Optional[GeoService] = None,
    ):
        self._orders = order_repo or OrderRepository()
        self._couriers = courier_repo or CourierRepository()
        self._geo = geo or GeoService()

    def get_all(self) -> dict:
        couriers = self._couriers.find_all()
        return {"couriers": couriers}

    def get_available(self) -> dict:
        couriers = self._couriers.find_available()
        return {"couriers": couriers, "count": len(couriers)}

    def get_by_id(self, courier_id: int) -> Optional[Dict]:
        return self._couriers.find_by_id(courier_id)

    def assign_order(self, courier_id: int, order_id: int) -> dict:
        courier = self._couriers.find_by_id(courier_id)
        if not courier:
            raise ValueError("Repartidor no encontrado")
        if not courier.get("available", True):
            raise ValueError("El repartidor no está disponible")

        order = self._orders.find_by_id(order_id)
        if not order:
            raise ValueError("Pedido no encontrado")
        if order.get("status") not in ["pendiente", "preparando"]:
            raise ValueError(f"El pedido no puede ser asignado. Estado actual: {order.get('status')}")

        order["courier_id"] = courier_id
        order["courier_name"] = courier["name"]
        order["courier_phone"] = courier["phone"]
        order["status"] = "en_camino"
        courier["available"] = False
        courier["current_order_id"] = order_id

        self._orders.update_and_save(order)
        self._couriers.update_and_save(courier)

        return {
            "message": f"Pedido {order_id} asignado a {courier['name']}",
            "order": order,
            "courier": courier,
        }

    def complete_order(self, courier_id: int, order_id: int) -> dict:
        courier = self._couriers.find_by_id(courier_id)
        if not courier:
            raise ValueError("Repartidor no encontrado")
        order = self._orders.find_by_id(order_id)
        if not order:
            raise ValueError("Pedido no encontrado")
        if order.get("courier_id") != courier_id:
            raise ValueError("Este pedido no está asignado a este repartidor")

        order["status"] = "entregado"
        courier["available"] = True
        courier["current_order_id"] = None

        self._orders.update_and_save(order)
        self._couriers.update_and_save(courier)

        return {
            "message": f"Pedido {order_id} marcado como entregado",
            "order": order,
            "courier": courier,
        }

    def get_nearby(self, lat: float, lng: float, max_distance: float = 5.0) -> dict:
        available = self._couriers.find_available()
        nearby = []
        for c in available:
            dist = self._geo.distance_km(lat, lng, c["lat"], c["lng"])
            if dist <= max_distance:
                copy = c.copy()
                copy["distance_km"] = round(dist, 2)
                nearby.append(copy)
        nearby.sort(key=lambda x: x["distance_km"])
        return {
            "couriers": nearby,
            "count": len(nearby),
            "location": {"lat": lat, "lng": lng},
            "max_distance_km": max_distance,
        }
