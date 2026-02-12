import json
import os
from datetime import datetime

from app.utils import DATA_DIR

LOG_FILE = os.path.join(DATA_DIR, "notifications.log")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")
OWNER_PHONE_DEFAULT = "+573022641006"


def _normalize_phone(phone: str) -> str:
    if not phone:
        return ""
    s = phone.strip().replace(" ", "").replace("-", "")
    if s.startswith("+57"):
        return s
    if s.startswith("57") and len(s) >= 11:
        return "+" + s
    if s.isdigit() and len(s) == 10:
        return "+57" + s
    if s.isdigit() and len(s) == 12 and s.startswith("57"):
        return "+" + s
    return "+57" + s.lstrip("0") if s.isdigit() else s


def _get_config():
    phone = os.environ.get("DELIVERY_OWNER_PHONE", "").strip()
    if phone:
        return {"owner_phone": _normalize_phone(phone)}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data.get("owner_phone"):
                    data["owner_phone"] = _normalize_phone(data["owner_phone"])
                return data
        except Exception:
            pass
    return {"owner_phone": OWNER_PHONE_DEFAULT}


def _build_sms_text(order: dict) -> str:
    lines = [
        "NUEVO PEDIDO #{}".format(order["id"]),
        "Negocio: {}".format(order.get("business_name", "—")),
        "Cliente: {}".format(order.get("customer_name", "—")),
        "Tel: {}".format(order.get("customer_phone", "—")),
        "Direccion: {}".format(order.get("customer_address", "—")),
        "Total: ${:,}".format(order.get("total", 0)),
        "Pago: {}".format(order.get("payment_method", "efectivo")),
    ]
    products = order.get("products") or []
    if products:
        lines.append("Productos:")
        for p in products[:5]:
            lines.append("  - {} x{} ${:,}".format(
                p.get("product_name", "?"),
                p.get("quantity", 0),
                p.get("subtotal", 0),
            ))
        if len(products) > 5:
            lines.append("  ... y {} mas".format(len(products) - 5))
    return "\n".join(lines)


def _log_and_print(message: str, order_id: int):
    os.makedirs(DATA_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = "[{}] Pedido #{} | SMS:\n{}\n---\n".format(timestamp, order_id, message)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception as e:
        print("⚠️ No se pudo escribir en el log:", e)
    print("\n📱 -------- SMS NOTIFICACIÓN (nuevo pedido) --------")
    print(message)
    print("📱 -------------------------------------------------\n")


def _send_twilio(to_phone: str, body: str) -> bool:
    sid = os.environ.get("TWILIO_ACCOUNT_SID", "").strip()
    token = os.environ.get("TWILIO_AUTH_TOKEN", "").strip()
    from_phone = os.environ.get("TWILIO_PHONE", "").strip()
    if not sid or not token or not from_phone:
        return False
    try:
        from twilio.rest import Client
        client = Client(sid, token)
        client.messages.create(body=body, from_=from_phone, to=to_phone)
        return True
    except Exception as e:
        print("⚠️ Error enviando SMS con Twilio:", e)
        return False


def send_new_order_sms(order: dict) -> None:
    message = _build_sms_text(order)
    order_id = order.get("id", 0)
    _log_and_print(message, order_id)

    config = _get_config()
    owner_phone = _normalize_phone(config.get("owner_phone") or "") or OWNER_PHONE_DEFAULT

    if _send_twilio(owner_phone, message):
        print("✅ SMS enviado a tu número:", owner_phone)
    else:
        print("💡 Las notificaciones se guardan en data/notifications.log y en esta consola.")
        print("   Para recibir SMS en", owner_phone, "configura Twilio (ver NOTIFICACIONES-SMS.md)")
