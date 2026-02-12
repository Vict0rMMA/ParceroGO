from fastapi import APIRouter

from app.routes.payments import process_payment_core

router = APIRouter()


@router.post("/pay")
async def orders_pay(payment_data: dict):
    return process_payment_core(payment_data)
