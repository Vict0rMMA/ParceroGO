"""
Prueba rápida de las notificaciones (SMS / log / consola).
No crea pedidos reales, solo dispara una notificación de prueba.

Ejecutar desde la carpeta del proyecto:
  python test_notification.py
"""

import sys
import os

# Asegurar que el proyecto esté en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Pedido de prueba (no se guarda en orders.json)
pedido_prueba = {
    "id": 999,
    "business_name": "Negocio de prueba",
    "customer_name": "Cliente prueba",
    "customer_phone": "+57 300 1112233",
    "customer_address": "Calle 50 #30-20, Medellín",
    "total": 45000,
    "payment_method": "efectivo",
    "products": [
        {"product_name": "Producto 1", "quantity": 2, "subtotal": 20000},
        {"product_name": "Producto 2", "quantity": 1, "subtotal": 25000},
    ],
}

def main():
    print("Enviando notificación de prueba a tu número (3022641006)...\n")
    try:
        from app.notify_sms import send_new_order_sms
        send_new_order_sms(pedido_prueba)
        print("Listo. Revisa:")
        print("  - Esta consola (arriba)")
        print("  - data/notifications.log")
        print("  - Tu celular (si Twilio está configurado)")
    except Exception as e:
        print("Error:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
