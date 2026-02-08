"""
Rutas para el módulo de repartidores.
Gestión de repartidores simulados: listado, asignación de pedidos y entrega.
"""

from fastapi import APIRouter, HTTPException

from app.utils import load_json, save_json, calculate_distance

router = APIRouter()

# -----------------------------------------------------------------------------
# Endpoints: Consulta de repartidores
# -----------------------------------------------------------------------------


@router.get("/")
async def get_couriers():
    """Devuelve todos los repartidores."""
    couriers = load_json("couriers.json")
    return {"couriers": couriers}


@router.get("/available")
async def get_available_couriers():
    """Devuelve solo repartidores disponibles (no ocupados)."""
    couriers = load_json("couriers.json")
    available = [c for c in couriers if c.get("available", True)]
    return {"couriers": available, "count": len(available)}


@router.get("/{courier_id}")
async def get_courier(courier_id: int):
    """Devuelve un repartidor por ID. 404 si no existe."""
    couriers = load_json("couriers.json")
    courier = next((c for c in couriers if c["id"] == courier_id), None)
    if not courier:
        raise HTTPException(status_code=404, detail="Repartidor no encontrado")
    return courier


# -----------------------------------------------------------------------------
# Endpoints: Asignación y entrega
# -----------------------------------------------------------------------------


@router.post("/{courier_id}/assign-order/{order_id}")
async def assign_order_to_courier(courier_id: int, order_id: int):
    """
    Asigna un pedido a un repartidor.
    El pedido debe estar en estado pendiente o preparando. El repartidor queda ocupado.
    """
    couriers = load_json("couriers.json")
    orders = load_json("orders.json")

    courier = next((c for c in couriers if c["id"] == courier_id), None)
    if not courier:
        raise HTTPException(status_code=404, detail="Repartidor no encontrado")
    if not courier.get("available", True):
        raise HTTPException(status_code=400, detail="El repartidor no está disponible")

    order = next((o for o in orders if o["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    if order.get("status") not in ["pendiente", "preparando"]:
        raise HTTPException(
            status_code=400,
            detail=f"El pedido no puede ser asignado. Estado actual: {order.get('status')}"
        )

    order["courier_id"] = courier_id
    order["courier_name"] = courier["name"]
    order["courier_phone"] = courier["phone"]
    order["status"] = "en_camino"
    courier["available"] = False
    courier["current_order_id"] = order_id

    save_json("orders.json", orders)
    save_json("couriers.json", couriers)

    return {
        "message": f"Pedido {order_id} asignado a {courier['name']}",
        "order": order,
        "courier": courier
    }


@router.post("/{courier_id}/complete-order/{order_id}")
async def complete_order(courier_id: int, order_id: int):
    """
    Marca el pedido como entregado y libera al repartidor.
    El pedido debe estar asignado a ese repartidor.
    """
    couriers = load_json("couriers.json")
    orders = load_json("orders.json")

    courier = next((c for c in couriers if c["id"] == courier_id), None)
    if not courier:
        raise HTTPException(status_code=404, detail="Repartidor no encontrado")

    order = next((o for o in orders if o["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    if order.get("courier_id") != courier_id:
        raise HTTPException(status_code=400, detail="Este pedido no está asignado a este repartidor")

    order["status"] = "entregado"
    courier["available"] = True
    courier["current_order_id"] = None

    save_json("orders.json", orders)
    save_json("couriers.json", couriers)

    return {
        "message": f"Pedido {order_id} marcado como entregado",
        "order": order,
        "courier": courier
    }


# -----------------------------------------------------------------------------
# Endpoints: Repartidores cercanos
# -----------------------------------------------------------------------------


@router.get("/nearby/{lat}/{lng}")
async def get_nearby_couriers(lat: float, lng: float, max_distance: float = 5.0):
    """
    Devuelve repartidores disponibles dentro de max_distance km de (lat, lng).
    Cada uno incluye distance_km. Ordenados por distancia ascendente.
    """
    couriers = load_json("couriers.json")
    available_couriers = [c for c in couriers if c.get("available", True)]

    nearby = []
    for courier in available_couriers:
        distance = calculate_distance(lat, lng, courier["lat"], courier["lng"])
        if distance <= max_distance:
            courier_copy = courier.copy()
            courier_copy["distance_km"] = round(distance, 2)
            nearby.append(courier_copy)

    nearby.sort(key=lambda x: x["distance_km"])

    return {
        "couriers": nearby,
        "count": len(nearby),
        "location": {"lat": lat, "lng": lng},
        "max_distance_km": max_distance
    }
