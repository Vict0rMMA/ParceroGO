from fastapi import APIRouter, HTTPException

from app.routes.payments import process_payment_core

router = APIRouter()


@router.post("/pay")
async def orders_pay(payment_data: dict):
    try:
        return process_payment_core(payment_data)
    except ValueError as e:
        if "no encontrado" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))
