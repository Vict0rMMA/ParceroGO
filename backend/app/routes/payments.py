from fastapi import APIRouter, HTTPException

from app.services.payment_service import PaymentService

router = APIRouter()
_payment_service = PaymentService()


def process_payment_core(payment_data: dict) -> dict:
    return _payment_service.process_payment(payment_data)


@router.post("/process")
async def process_payment(payment_data: dict):
    try:
        return process_payment_core(payment_data)
    except ValueError as e:
        if "no encontrado" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/history")
async def get_payment_history():
    return _payment_service.get_history()


@router.get("/orders/{order_id}/payment")
async def get_order_payment(order_id: int):
    try:
        return _payment_service.get_order_payment(order_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
