import os

TO_PHONE = "+573022641006"
MENSAJE_PAGO_OK = (
    "Pedido confirmado. Tu pago fue exitoso y el pedido esta en preparacion."
)


def send_order_sms() -> bool:
    sid = os.environ.get("TWILIO_ACCOUNT_SID", "").strip()
    token = os.environ.get("TWILIO_AUTH_TOKEN", "").strip()
    from_phone = os.environ.get("TWILIO_PHONE", "").strip()

    if not sid or not token or not from_phone:
        return False

    try:
        from twilio.rest import Client
        client = Client(sid, token)
        client.messages.create(
            body=MENSAJE_PAGO_OK,
            from_=from_phone,
            to=TO_PHONE,
        )
        return True
    except Exception:
        return False
