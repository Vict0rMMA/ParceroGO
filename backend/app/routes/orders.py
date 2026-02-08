"""
Rutas de pedidos: endpoint de pago que dispara SMS de confirmación.
Redirige la lógica al módulo de pagos (process_payment_core).
"""

from fastapi import APIRouter

from app.routes.payments import process_payment_core

router = APIRouter()

# -----------------------------------------------------------------------------
# Endpoint: Pago desde flujo de pedidos
# -----------------------------------------------------------------------------


@router.post("/pay")
async def orders_pay(payment_data: dict):
    """
    Procesa un pago simulado. Si es exitoso, envía SMS de confirmación.
    Responde siempre (aunque el SMS falle).
    Body: order_id, payment_method; si es tarjeta: card_number, card_holder, cvv.
    """
    return process_payment_core(payment_data)
