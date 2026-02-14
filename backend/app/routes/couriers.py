from fastapi import APIRouter, HTTPException

from app.services.courier_service import CourierService

router = APIRouter()
_courier_service = CourierService()


def _to_404(e: ValueError) -> bool:
    return "no encontrado" in str(e).lower()


@router.get("/")
async def get_couriers():
    return _courier_service.get_all()


@router.get("/available")
async def get_available_couriers():
    return _courier_service.get_available()


@router.get("/{courier_id}")
async def get_courier(courier_id: int):
    courier = _courier_service.get_by_id(courier_id)
    if not courier:
        raise HTTPException(status_code=404, detail="Repartidor no encontrado")
    return courier


@router.post("/{courier_id}/assign-order/{order_id}")
async def assign_order_to_courier(courier_id: int, order_id: int):
    try:
        return _courier_service.assign_order(courier_id, order_id)
    except ValueError as e:
        raise HTTPException(status_code=404 if _to_404(e) else 400, detail=str(e))


@router.post("/{courier_id}/complete-order/{order_id}")
async def complete_order(courier_id: int, order_id: int):
    try:
        return _courier_service.complete_order(courier_id, order_id)
    except ValueError as e:
        raise HTTPException(status_code=404 if _to_404(e) else 400, detail=str(e))


@router.get("/nearby/{lat}/{lng}")
async def get_nearby_couriers(lat: float, lng: float, max_distance: float = 5.0):
    return _courier_service.get_nearby(lat, lng, max_distance)
