from typing import Dict, Optional

from app.repositories.order_repository import OrderRepository
from app.repositories.payment_repository import PaymentRepository
from app.utils import get_current_timestamp


class PaymentService:
    VALID_METHODS = ["efectivo", "tarjeta"]

    def __init__(
        self,
        order_repo: Optional[OrderRepository] = None,
        payment_repo: Optional[PaymentRepository] = None,
    ):
        self._orders = order_repo or OrderRepository()
        self._payments = payment_repo or PaymentRepository()

    def process_payment(self, payment_data: dict) -> dict:
        order = self._orders.find_by_id(payment_data["order_id"])
        if not order:
            raise ValueError("Pedido no encontrado")
        if order.get("payment_status") == "pagado":
            raise ValueError("El pedido ya está pagado")

        payment_method = payment_data.get("payment_method", "efectivo")
        if payment_method not in self.VALID_METHODS:
            raise ValueError(f"Método de pago inválido. Válidos: {', '.join(self.VALID_METHODS)}")

        if payment_method == "tarjeta":
            card_number = payment_data.get("card_number", "").replace(" ", "").replace("-", "")
            if not card_number or len(card_number) < 13 or len(card_number) > 19:
                raise ValueError("Número de tarjeta inválido. Debe tener entre 13 y 19 dígitos")
            if not card_number.isdigit():
                raise ValueError("El número de tarjeta solo puede contener dígitos")
            if not payment_data.get("card_holder") or len(payment_data["card_holder"].strip()) < 3:
                raise ValueError("Nombre del titular requerido (mínimo 3 caracteres)")
            cvv = payment_data.get("cvv", "")
            if not cvv or len(cvv) != 3 or not cvv.isdigit():
                raise ValueError("CVV inválido. Debe ser un número de 3 dígitos")
            payment_status = "pagado"
            payment_message = "Pago con tarjeta procesado exitosamente"
        else:
            payment_status = "pendiente"
            payment_message = "Pago en efectivo registrado. Se cobrará al momento de la entrega."

        order["payment_method"] = payment_method
        order["payment_status"] = payment_status

        payments = self._payments.find_all()
        tip_amount = order.get("tip_amount") or 0
        payment_record = {
            "id": len(payments) + 1,
            "order_id": order["id"],
            "amount": order["total"],
            "tip_amount": tip_amount,
            "payment_method": payment_method,
            "status": payment_status,
            "created_at": get_current_timestamp(),
        }
        self._payments.append_and_save(payment_record)
        self._orders.update_and_save(order)

        try:
            from app.sms_service import send_order_sms
            send_order_sms()
        except Exception:
            pass

        return {
            "payment": payment_record,
            "message": payment_message,
            "order": order,
        }

    def get_history(self) -> dict:
        payments = self._payments.find_all()
        return {"payments": payments}

    def get_order_payment(self, order_id: int) -> dict:
        order = self._orders.find_by_id(order_id)
        if not order:
            raise ValueError("Pedido no encontrado")
        payment = self._payments.find_by_order_id(order_id)
        return {
            "order_id": order_id,
            "total": order["total"],
            "payment_method": order.get("payment_method", "efectivo"),
            "payment_status": order.get("payment_status", "pendiente"),
            "payment_record": payment,
        }
