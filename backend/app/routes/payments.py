"""
Rutas para el módulo de pagos.
Sistema de pago simulado: efectivo y tarjeta. Tras pago exitoso se envía SMS de confirmación.
"""

from fastapi import APIRouter, HTTPException

from app.utils import load_json, save_json, get_current_timestamp

router = APIRouter()

# -----------------------------------------------------------------------------
# Lógica central de pago (reutilizada por POST /process y por orders /pay)
# -----------------------------------------------------------------------------


def process_payment_core(payment_data: dict) -> dict:
    """
    Procesa un pago simulado de forma síncrona.
    - Valida pedido, método de pago y (si es tarjeta) número, titular y CVV.
    - Actualiza payment_status del pedido y guarda el registro en payments.json.
    - Si el pago es exitoso, intenta enviar SMS (el fallo del SMS no afecta la respuesta).
    Returns: dict con "payment", "message", "order".
    """
    orders = load_json("orders.json")
    order = next((o for o in orders if o["id"] == payment_data["order_id"]), None)

    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    if order["payment_status"] == "pagado":
        raise HTTPException(status_code=400, detail="El pedido ya está pagado")

    payment_method = payment_data.get("payment_method", "efectivo")
    valid_payment_methods = ["efectivo", "tarjeta"]
    if payment_method not in valid_payment_methods:
        raise HTTPException(
            status_code=400,
            detail=f"Método de pago inválido. Válidos: {', '.join(valid_payment_methods)}"
        )

    if payment_method == "tarjeta":
        card_number = payment_data.get("card_number", "").replace(" ", "").replace("-", "")
        if not card_number or len(card_number) < 13 or len(card_number) > 19:
            raise HTTPException(
                status_code=400,
                detail="Número de tarjeta inválido. Debe tener entre 13 y 19 dígitos"
            )
        if not card_number.isdigit():
            raise HTTPException(status_code=400, detail="El número de tarjeta solo puede contener dígitos")
        if not payment_data.get("card_holder") or len(payment_data["card_holder"].strip()) < 3:
            raise HTTPException(
                status_code=400,
                detail="Nombre del titular requerido (mínimo 3 caracteres)"
            )
        cvv = payment_data.get("cvv", "")
        if not cvv or len(cvv) != 3 or not cvv.isdigit():
            raise HTTPException(status_code=400, detail="CVV inválido. Debe ser un número de 3 dígitos")

        payment_status = "pagado"
        payment_message = "Pago con tarjeta procesado exitosamente"
    else:
        payment_status = "pendiente"
        payment_message = "Pago en efectivo registrado. Se cobrará al momento de la entrega."

    order["payment_method"] = payment_method
    order["payment_status"] = payment_status

    payments = load_json("payments.json")
    tip_amount = order.get("tip_amount") or 0
    payment_record = {
        "id": len(payments) + 1,
        "order_id": order["id"],
        "amount": order["total"],
        "tip_amount": tip_amount,
        "payment_method": payment_method,
        "status": payment_status,
        "created_at": get_current_timestamp()
    }
    payments.append(payment_record)
    save_json("payments.json", payments)
    save_json("orders.json", orders)

    try:
        from app.sms_service import send_order_sms
        send_order_sms()
    except Exception:
        pass

    return {
        "payment": payment_record,
        "message": payment_message,
        "order": order
    }


# -----------------------------------------------------------------------------
# Endpoints de pagos
# -----------------------------------------------------------------------------


@router.post("/process")
async def process_payment(payment_data: dict):
    """
    Procesa un pago simulado.
    Body: order_id, payment_method ("efectivo"|"tarjeta"), y si es tarjeta: card_number, card_holder, cvv.
    """
    return process_payment_core(payment_data)


@router.get("/history")
async def get_payment_history():
    """Devuelve el historial de pagos registrados."""
    payments = load_json("payments.json")
    return {"payments": payments}


@router.get("/orders/{order_id}/payment")
async def get_order_payment(order_id: int):
    """Devuelve la información de pago asociada a un pedido."""
    orders = load_json("orders.json")
    order = next((o for o in orders if o["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    payments = load_json("payments.json")
    payment = next((p for p in payments if p["order_id"] == order_id), None)

    return {
        "order_id": order_id,
        "total": order["total"],
        "payment_method": order.get("payment_method", "efectivo"),
        "payment_status": order.get("payment_status", "pendiente"),
        "payment_record": payment
    }
