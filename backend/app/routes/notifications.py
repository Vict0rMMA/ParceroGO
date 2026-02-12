from datetime import datetime

from fastapi import APIRouter, HTTPException

from app.utils import load_json

router = APIRouter()


@router.post("/send-sms")
async def send_sms_notification(notification_data: dict):
    phone = notification_data.get("phone")
    message = notification_data.get("message")
    order_id = notification_data.get("order_id")

    if not phone or not message:
        raise HTTPException(status_code=400, detail="Teléfono y mensaje son requeridos")

    print(f"📱 [SMS SIMULADO] Enviado a {phone}: {message}")

    return {
        "success": True,
        "message": "Notificación SMS enviada (simulado)",
        "phone": phone,
        "order_id": order_id,
        "timestamp": datetime.now().isoformat()
    }


@router.post("/notify-order-status/{order_id}")
async def notify_order_status_change(order_id: int):
    orders = load_json("orders.json")
    order = next((o for o in orders if o["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    status_messages = {
        "pendiente": f"Tu pedido #{order_id} ha sido recibido y está siendo procesado.",
        "preparando": f"Tu pedido #{order_id} está siendo preparado por {order['business_name']}.",
        "en_camino": f"¡Tu pedido #{order_id} está en camino! Repartidor: {order.get('delivery_person', 'Asignado')}",
        "entregado": f"✅ Tu pedido #{order_id} ha sido entregado exitosamente. ¡Gracias por tu compra!",
        "cancelado": f"Tu pedido #{order_id} ha sido cancelado."
    }
    message = status_messages.get(order["status"], f"El estado de tu pedido #{order_id} ha cambiado.")

    print(f"📱 [NOTIFICACIÓN] Pedido #{order_id} - Estado: {order['status']}")
    print(f"   Mensaje: {message}")
    print(f"   Teléfono: {order['customer_phone']}")

    return {
        "success": True,
        "order_id": order_id,
        "status": order["status"],
        "message": message,
        "notification_sent": True
    }
