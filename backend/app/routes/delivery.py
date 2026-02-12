from datetime import datetime
from typing import List, Dict, Optional

from fastapi import APIRouter, HTTPException

from app.utils import (
    load_json,
    save_json,
    calculate_distance,
    get_current_timestamp,
    validate_coordinates,
)

router = APIRouter()


def _normalize_phone_for_match(phone: str) -> str:
    if not phone:
        return ""
    s = "".join(c for c in str(phone) if c.isdigit())
    return s[2:] if len(s) == 12 and s.startswith("57") else s


def _get_all_products() -> List[Dict]:
    return load_json("products.json")


def _find(seq: list, key: str, value) -> Optional[Dict]:
    return next((x for x in seq if x.get(key) == value), None)


@router.get("/businesses")
async def get_businesses():
    businesses = load_json("businesses.json")
    return {"businesses": businesses}


@router.get("/businesses/{business_id}")
async def get_business(business_id: int):
    businesses = load_json("businesses.json")
    business = _find(businesses, "id", business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    return business


@router.get("/businesses/{business_id}/products")
async def get_business_products(business_id: int):
    products = load_json("products.json")
    business_products = [
        p for p in products
        if p["business_id"] == business_id and p.get("available", True)
    ]
    return {"products": business_products}


@router.get("/products")
async def get_all_products(category: str = None):
    all_products = _get_all_products()
    if category:
        all_products = [p for p in all_products if p.get("category", "").lower() == category.lower()]
    return {"products": all_products, "count": len(all_products), "category": category}


@router.post("/orders")
async def create_order(order_data: dict):
    orders = load_json("orders.json")
    all_products = _get_all_products()
    businesses = load_json("businesses.json")
    business = _find(businesses, "id", order_data["business_id"])
    if not business:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")

    total = 0
    order_products = []
    for item in order_data["products"]:
        product = _find(all_products, "id", item["product_id"])
        if not product:
            raise HTTPException(status_code=404, detail=f"Producto {item['product_id']} no encontrado")
        if not product.get("available", True):
            raise HTTPException(status_code=400, detail=f"Producto {product['name']} no disponible")

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
            "notes": notes
        })

    if not validate_coordinates(order_data["customer_lat"], order_data["customer_lng"]):
        raise HTTPException(
            status_code=400,
            detail="Coordenadas fuera del rango válido para Medellín"
        )

    if not order_products:
        raise HTTPException(status_code=400, detail="El pedido debe contener al menos un producto")

    tip_amount = int(order_data.get("tip_amount") or 0)
    if tip_amount < 0:
        tip_amount = 0
    total += tip_amount

    distance = calculate_distance(
        business["latitude"], business["longitude"],
        order_data["customer_lat"], order_data["customer_lng"]
    )
    estimated_time = int(business.get("delivery_time", 30) + (distance * 2))

    new_order = {
        "id": len(orders) + 1,
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
        "tip_amount": int(order_data.get("tip_amount") or 0),
        "payment_status": "pendiente",
        "status": "pendiente",
        "delivery_person": None,
        "courier_phone": None,
        "created_at": get_current_timestamp(),
        "status_history": [{
            "status": "pendiente",
            "timestamp": datetime.now().isoformat()
        }]
    }

    orders.append(new_order)
    save_json("orders.json", orders)

    try:
        from app.notify_sms import send_new_order_sms
        send_new_order_sms(new_order)
    except Exception as e:
        print("⚠️ Notificación de pedido no enviada:", e)

    return {"order": new_order, "message": "Pedido creado exitosamente"}


@router.get("/orders")
async def get_orders(courier_id: int = None, business_id: int = None):
    orders = load_json("orders.json")
    if courier_id is not None:
        orders = [o for o in orders if o.get("courier_id") == courier_id]
    if business_id is not None:
        orders = [o for o in orders if o.get("business_id") == business_id]
    return {"orders": orders, "count": len(orders)}


@router.get("/orders/by-phone/{phone}")
async def get_orders_by_phone(phone: str):
    orders = load_json("orders.json")
    normalized_search = _normalize_phone_for_match(phone)
    customer_orders = [
        o for o in orders
        if _normalize_phone_for_match(o.get("customer_phone", "")) == normalized_search
    ]
    customer_orders.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return {"orders": customer_orders, "count": len(customer_orders)}


@router.get("/orders/{order_id}")
async def get_order(order_id: int):
    orders = load_json("orders.json")
    order = _find(orders, "id", order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return {"order": order}


@router.patch("/orders/{order_id}/status")
async def update_order_status(order_id: int, status_data: dict):
    orders = load_json("orders.json")
    order = _find(orders, "id", order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    old_status = order["status"]
    new_status = status_data.get("status")
    valid_statuses = ["pendiente", "preparando", "en_camino", "entregado", "cancelado"]
    if new_status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Válidos: {valid_statuses}")

    order["status"] = new_status
    courier_id = status_data.get("courier_id")

    if new_status == "en_camino":
        if courier_id:
            couriers = load_json("couriers.json")
            courier = _find(couriers, "id", courier_id)
            if courier:
                order["courier_id"] = courier_id
                order["delivery_person"] = courier.get("name", "")
                order["courier_phone"] = courier.get("phone", "")
        elif not order.get("delivery_person"):
            delivery_persons = ["Carlos", "María", "Pedro", "Ana"]
            order["delivery_person"] = f"{delivery_persons[order_id % len(delivery_persons)]}"
            order["courier_phone"] = f"+57 300 {1000000 + order_id}"

    if "status_history" not in order:
        order["status_history"] = []
    order["status_history"].append({
        "status": new_status,
        "timestamp": datetime.now().isoformat()
    })
    order["updated_at"] = datetime.now().isoformat()

    save_json("orders.json", orders)

    print(f"📱 [NOTIFICACIÓN] Pedido #{order_id} cambió de '{old_status}' a '{new_status}'")
    print(f"   Cliente: {order['customer_name']} - Teléfono: {order['customer_phone']}")

    return {"order": order, "message": f"Estado actualizado de '{old_status}' a '{new_status}'"}


@router.get("/delivery-persons")
async def get_delivery_persons():
    couriers = load_json("couriers.json")
    return {"delivery_persons": couriers}


@router.get("/cart")
async def get_cart():
    return {
        "items": [],
        "total": 0,
        "item_count": 0
    }


@router.post("/cart/add")
async def add_to_cart(cart_item: dict):
    all_products = _get_all_products()
    product = _find(all_products, "id", cart_item["product_id"])
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if not product.get("available", True):
        raise HTTPException(status_code=400, detail=f"Producto {product['name']} no disponible")

    quantity = cart_item.get("quantity", 1)

    return {
        "success": True,
        "product": {
            "id": product["id"],
            "name": product["name"],
            "price": product["price"],
            "image": product.get("image", ""),
            "category": product.get("category", ""),
            "quantity": quantity,
            "subtotal": product["price"] * quantity
        },
        "message": f"{product['name']} agregado al carrito"
    }


@router.delete("/cart/remove/{product_id}")
async def remove_from_cart(product_id: int):
    all_products = _get_all_products()
    product = _find(all_products, "id", product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return {
        "success": True,
        "product_id": product_id,
        "message": f"{product['name']} removido del carrito"
    }
