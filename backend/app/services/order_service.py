from datetime import datetime
from typing import List, Dict, Optional

from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.business_repository import BusinessRepository
from app.repositories.courier_repository import CourierRepository
from app.services.geo_service import GeoService
from app.utils import get_current_timestamp


class OrderService:
    VALID_STATUSES = ["pendiente", "preparando", "en_camino", "entregado", "cancelado"]

    def __init__(
        self,
        order_repo: Optional[OrderRepository] = None,
        product_repo: Optional[ProductRepository] = None,
        business_repo: Optional[BusinessRepository] = None,
        courier_repo: Optional[CourierRepository] = None,
        geo: Optional[GeoService] = None,
    ):
        self._orders = order_repo or OrderRepository()
        self._products = product_repo or ProductRepository()
        self._businesses = business_repo or BusinessRepository()
        self._couriers = courier_repo or CourierRepository()
        self._geo = geo or GeoService()

    def create_order(self, order_data: dict) -> dict:
        business = self._businesses.find_by_id(order_data["business_id"])
        if not business:
            raise ValueError("Negocio no encontrado")

        all_products = self._products.find_all()
        total = 0
        order_products = []
        for item in order_data["products"]:
            product = next((p for p in all_products if p.get("id") == item["product_id"]), None)
            if not product:
                raise ValueError(f"Producto {item['product_id']} no encontrado")
            if not product.get("available", True):
                raise ValueError(f"Producto {product['name']} no disponible")
            quantity = item.get("quantity", 1)
            notes = (item.get("notes") or "").strip()[:500]
            subtotal = product["price"] * quantity
            total += subtotal
            order_products.append({
                "product_id": product["id"],
                "product_name": product["name"],
                "quantity": quantity,
                "unit_price": product["price"],
                "subtotal": subtotal,
                "notes": notes,
            })

        if not self._geo.are_valid_for_medellin(order_data["customer_lat"], order_data["customer_lng"]):
            raise ValueError("Coordenadas fuera del rango válido para Medellín")
        if not order_products:
            raise ValueError("El pedido debe contener al menos un producto")

        tip_amount = int(order_data.get("tip_amount") or 0)
        if tip_amount < 0:
            tip_amount = 0
        total += tip_amount

        distance = self._geo.distance_km(
            business["latitude"], business["longitude"],
            order_data["customer_lat"], order_data["customer_lng"],
        )
        estimated_time = int(business.get("delivery_time", 30) + (distance * 2))

        orders = self._orders.find_all()
        new_id = len(orders) + 1
        new_order = {
            "id": new_id,
            "customer_name": order_data["customer_name"],
            "customer_phone": order_data["customer_phone"],
            "customer_address": order_data["customer_address"],
            "customer_lat": order_data["customer_lat"],
            "customer_lng": order_data["customer_lng"],
            "business_id": business["id"],
            "business_name": business["name"],
            "business_lat": business["latitude"],
            "business_lng": business["longitude"],
            "products": order_products,
            "total": total,
            "distance_km": round(distance, 2),
            "estimated_time": estimated_time,
            "payment_method": order_data.get("payment_method", "efectivo"),
            "tip_amount": tip_amount,
            "payment_status": "pendiente",
            "status": "pendiente",
            "delivery_person": None,
            "courier_phone": None,
            "created_at": get_current_timestamp(),
            "status_history": [{"status": "pendiente", "timestamp": datetime.now().isoformat()}],
        }
        self._orders.append_and_save(new_order)

        try:
            from app.notify_sms import send_new_order_sms
            send_new_order_sms(new_order)
        except Exception as e:
            print("⚠️ Notificación de pedido no enviada:", e)

        return {"order": new_order, "message": "Pedido creado exitosamente"}

    def get_orders(self, courier_id: Optional[int] = None, business_id: Optional[int] = None) -> dict:
        orders = self._orders.find_all()
        if courier_id is not None:
            orders = [o for o in orders if o.get("courier_id") == courier_id]
        if business_id is not None:
            orders = [o for o in orders if o.get("business_id") == business_id]
        return {"orders": orders, "count": len(orders)}

    def get_orders_by_phone(self, phone: str) -> dict:
        normalized = OrderRepository._normalize_phone(phone)
        customer_orders = self._orders.find_by_phone_normalized(normalized)
        customer_orders.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return {"orders": customer_orders, "count": len(customer_orders)}

    def get_order_by_id(self, order_id: int) -> Optional[Dict]:
        return self._orders.find_by_id(order_id)

    def update_status(self, order_id: int, status_data: dict) -> dict:
        order = self._orders.find_by_id(order_id)
        if not order:
            raise ValueError("Pedido no encontrado")

        old_status = order["status"]
        new_status = status_data.get("status")
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Estado inválido. Válidos: {self.VALID_STATUSES}")

        order["status"] = new_status
        courier_id = status_data.get("courier_id")

        if new_status == "en_camino":
            if courier_id:
                courier = self._couriers.find_by_id(courier_id)
                if courier:
                    order["courier_id"] = courier_id
                    order["delivery_person"] = courier.get("name", "")
                    order["courier_phone"] = courier.get("phone", "")
            elif not order.get("delivery_person"):
                delivery_persons = ["Carlos", "María", "Pedro", "Ana"]
                order["delivery_person"] = delivery_persons[order_id % len(delivery_persons)]
                order["courier_phone"] = f"+57 300 {1000000 + order_id}"

        if "status_history" not in order:
            order["status_history"] = []
        order["status_history"].append({
            "status": new_status,
            "timestamp": datetime.now().isoformat(),
        })
        order["updated_at"] = datetime.now().isoformat()

        self._orders.update_and_save(order)

        print(f"📱 [NOTIFICACIÓN] Pedido #{order_id} cambió de '{old_status}' a '{new_status}'")
        print(f"   Cliente: {order['customer_name']} - Teléfono: {order['customer_phone']}")

        return {"order": order, "message": f"Estado actualizado de '{old_status}' a '{new_status}'"}
