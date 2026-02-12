# ParceroGO — Explicación del código y preguntas que puede hacer el profe

---

## 1. QUÉ ES EL PROYECTO

**ParceroGO** es un **MVP (Producto Mínimo Viable)** de una app de **delivery local** para negocios de barrio en Medellín.  
No usa base de datos real: todo se guarda en **archivos JSON**. Los pagos y los SMS son **simulados** (no hay transacciones ni envíos reales).

---

## 2. ARQUITECTURA GENERAL

```
[Usuario] → Navegador (HTML + JS) → FastAPI (backend) → Archivos JSON (data/)
                ↑                           ↓
            Leaflet (mapa)              utils.py (distancia, carga/guardado)
```

- **Backend:** FastAPI (Python). Sirve páginas HTML y expone APIs REST.
- **Frontend:** HTML, CSS y JavaScript puro (sin React/Vue). Mapa con **Leaflet** + OpenStreetMap.
- **Datos:** Carpeta `data/` con `businesses.json`, `products.json`, `couriers.json`, `orders.json`, `payments.json`.

---

## 3. EXPLICACIÓN POR PARTES

### 3.1 Backend — `backend/app/main.py`

- Carga variables de entorno desde `.env` si existe (por ejemplo para configuración).
- Crea la app FastAPI y **monta**:
  - `/static` → archivos estáticos (CSS, JS, imágenes).
  - **Jinja2** para renderizar plantillas HTML desde `frontend/templates/`.
- **Routers (APIs):**
  - `/api/delivery` → negocios, productos, pedidos.
  - `/api/payments` → procesar pago (efectivo/tarjeta simulado).
  - `/api/couriers` → repartidores, asignar pedido, repartidores cercanos.
  - `/api/notifications` → envío de SMS simulado.
  - `/orders/pay` → atajo para pagar un pedido.
- **Rutas HTML:** cada ruta (ej. `/`, `/delivery`, `/checkout`, `/tracking`, `/repartidor`) devuelve una plantilla HTML.

**Posible pregunta:** *¿Qué es FastAPI y para qué lo usaron?*  
→ Framework de Python para crear APIs REST y servir la app. Permite definir rutas, validar datos y documentación automática (en este proyecto las docs están desactivadas con `docs_url=None`).

---

### 3.2 Utilidades — `backend/app/utils.py`

- **`load_json(file_name)`** / **`save_json(file_name, data)`**: leen y escriben JSON en la carpeta `data/`. Así se “persiste” sin base de datos.
- **`calculate_distance(lat1, lng1, lat2, lng2)`**: calcula la distancia en **km** entre dos puntos con la **fórmula de Haversine** (considera la Tierra como esfera, radio ≈ 6371 km).
- **`get_current_timestamp()`**: devuelve la fecha/hora actual en formato ISO (para `created_at`, etc.).
- **`validate_coordinates(lat, lng)`**: comprueba que las coordenadas estén dentro de un rango aproximado de Medellín (lat 6.0–6.5, lng -75.8 a -75.4).

**Posible pregunta:** *¿Cómo calculan la distancia entre negocio y cliente?*  
→ Con la fórmula de Haversine en `utils.py`, que calcula la distancia en línea recta sobre la esfera terrestre (en km). Se usa para el tiempo estimado de entrega y para repartidores cercanos.

---

### 3.3 Delivery (pedidos) — `backend/app/routes/delivery.py`

- **GET `/businesses`**: lista todos los negocios desde `businesses.json`.
- **GET `/businesses/{id}/products`**: productos de un negocio (filtrados por `business_id` y disponibles).
- **POST `/orders`**: crea un pedido.  
  - Valida negocio, productos, cantidades, coordenadas del cliente.  
  - Calcula total (productos + propina).  
  - Calcula distancia (Haversine) y tiempo estimado.  
  - Guarda el pedido en `orders.json` con estado `pendiente` y `status_history`.  
  - Opcionalmente registra notificación de nuevo pedido (simulado).
- **GET `/orders`**: lista pedidos (opcionalmente por `courier_id` o `business_id`).
- **GET `/orders/by-phone/{phone}`**: pedidos de un cliente por teléfono (normaliza número para comparar).
- **PATCH `/orders/{id}/status`**: cambia estado del pedido (`pendiente`, `preparando`, `en_camino`, `entregado`, `cancelado`). Si se pone `en_camino` se puede asignar repartidor (`courier_id`) y se actualiza `delivery_person` y `courier_phone`.

**Posible pregunta:** *¿Cómo se crea un pedido y qué validaciones tienen?*  
→ Se envía un POST con `business_id`, `products` (id, cantidad, notas), datos del cliente (nombre, teléfono, dirección, lat/lng), método de pago y propina. Se valida que el negocio exista, que los productos existan y estén disponibles, que las coordenadas estén en Medellín y que haya al menos un producto. Luego se calcula total, distancia y tiempo y se guarda en JSON.

---

### 3.4 Pagos — `backend/app/routes/payments.py`

- **POST `/process`**: procesa el pago de un pedido (simulado).  
  - **Efectivo:** solo registra “pendiente”, mensaje de que se cobra en la entrega.  
  - **Tarjeta:** valida número (13–19 dígitos), titular (mín. 3 caracteres), CVV (3 dígitos). Marca el pedido como `pagado` y guarda un registro en `payments.json`.
- **GET `/history`**: historial de pagos.
- **GET `/orders/{id}/payment`**: estado de pago de un pedido.

**Posible pregunta:** *¿Los pagos son reales?*  
→ No. Son simulados: no hay pasarela (Mercado Pago, Stripe, etc.). Solo se validan formato y se actualiza estado en JSON.

---

### 3.5 Repartidores — `backend/app/routes/couriers.py`

- **GET `/available`**: repartidores con `available: true`.
- **POST `/{courier_id}/assign-order/{order_id}`**: asigna un pedido a un repartidor. El pedido debe estar `pendiente` o `preparando`. Se pone estado `en_camino`, el repartidor pasa a no disponible y se guarda `current_order_id`.
- **POST `/{courier_id}/complete-order/{order_id}`**: marca pedido como `entregado`, repartidor vuelve a disponible.
- **GET `/nearby/{lat}/{lng}`**: repartidores disponibles a menos de X km (por defecto 5) usando `calculate_distance` (Haversine), ordenados por distancia.

**Posible pregunta:** *¿Cómo eligen al repartidor?*  
→ Por cercanía: se usa la API de repartidores cercanos (`/nearby/lat/lng`) que calcula la distancia con Haversine y ordena por distancia. La asignación real se hace en el panel repartidor (asignar/completar pedido).

---

### 3.6 Notificaciones — `backend/app/routes/notifications.py`

- **POST `/send-sms`**: “envía” un SMS; en realidad solo imprime en consola (simulado).
- **POST `/notify-order-status/{order_id}`**: genera el mensaje según estado del pedido y lo imprime (simulado).

---

### 3.7 Generación de datos — `backend/app/data_generator.py` y `backend/init_data.py`

- **`data_generator.py`**:  
  - Listas de ubicaciones en Medellín (El Poblado, Laureles, etc.).  
  - Genera **negocios** con nombre, categoría, dirección, lat/lng, teléfono, rating, `delivery_time`.  
  - Genera **productos** por categoría (Restaurante, Pizzería, Farmacia, etc.) asociados a cada negocio (3–5 productos por negocio).  
  - Genera **repartidores** con nombre, teléfono, lat/lng, zona, disponible, vehículo, rating.
- **`init_data.py`**: script que llama a `generate_businesses`, `generate_products`, `generate_couriers` y escribe `businesses.json`, `products.json`, `couriers.json`, y crea `orders.json` y `payments.json` vacíos si no existen.

**Posible pregunta:** *¿De dónde salen los negocios y productos?*  
→ Se generan con el script `init_data.py` usando `data_generator.py`: datos aleatorios pero coherentes (ubicaciones en Medellín, productos por categoría). No hay scraping ni BD externa en el flujo principal.

---

### 3.8 Frontend — mapa y flujo

- **Leaflet:** librería para el mapa. Centro en Medellín (6.2476, -75.5658). Tiles de CartoDB (OpenStreetMap).
- **`delivery.js`**: carga negocios y repartidores, los muestra como marcadores en el mapa; filtros por categoría, búsqueda, favoritos en `localStorage`; carrito en memoria y llamadas a `/api/delivery/...` para productos y creación de pedidos.
- **Tracking:** la página de tracking permite buscar pedido por ID o teléfono (GET `/api/delivery/orders/by-phone/{phone}`), muestra estado y timeline (pendiente → preparando → en camino → entregado).

**Posible pregunta:** *¿Qué tecnología usan para el mapa?*  
→ Leaflet.js con OpenStreetMap (tiles CartoDB). Las coordenadas son de Medellín y la distancia se calcula con Haversine en el backend.

---

## 4. FLUJO DE UN PEDIDO (RESUMEN)

1. Usuario entra a **Delivery**, ve mapa con negocios, elige uno y agrega productos al carrito.
2. Va a **Checkout**, ingresa nombre, teléfono, dirección (y opcionalmente ubicación). Envía **POST `/api/delivery/orders`** con negocio, productos, datos del cliente, método de pago, propina.
3. Backend valida, calcula total y distancia, guarda en `orders.json`.
4. Usuario puede ir a **Pagos** y hacer **POST `/api/payments/process`** (efectivo o tarjeta simulado). Se actualiza `payment_status` y se guarda en `payments.json`.
5. En **Tracking**, el usuario busca por teléfono; se llama **GET `/api/delivery/orders/by-phone/{phone}`** y se muestra el estado y la línea de tiempo.
6. Un repartidor en **Panel repartidor** puede asignar el pedido (POST en couriers) y cambiar estado a preparando → en camino → entregado (PATCH `/api/delivery/orders/{id}/status`).

---

## 5. PREGUNTAS QUE PUEDE HACER EL PROFE (Y CÓMO CONTESTAR)

| Pregunta | Respuesta corta |
|----------|------------------|
| ¿Qué es este proyecto? | MVP de delivery local para Medellín: mapa con negocios, carrito, pedidos, pagos y tracking simulados; sin BD, todo en JSON. |
| ¿Por qué no usan base de datos? | Es un MVP académico; JSON permite desarrollar rápido sin configurar BD. Para producción se usaría una BD real. |
| ¿Cómo calculan la distancia? | Fórmula de Haversine en `utils.py`: considera la Tierra como esfera de radio 6371 km. |
| ¿Los pagos son reales? | No. Son simulados: solo se valida formato (tarjeta, CVV, titular) y se actualiza estado en JSON. No hay pasarela de pago. |
| ¿Qué es FastAPI? | Framework de Python para APIs REST: rutas, validación, tipos. En el proyecto sirve también las páginas HTML con Jinja2. |
| ¿Qué es Leaflet? | Librería JavaScript para mapas interactivos. Aquí se usa con OpenStreetMap (CartoDB) centrado en Medellín. |
| ¿Cómo se asignan los repartidores? | Por cercanía: se obtienen repartidores disponibles cerca del punto (Haversine) y se asigna manualmente en el panel; el estado del pedido pasa a “en camino”. |
| ¿Dónde se guardan los pedidos? | En `data/orders.json`. Se lee y escribe con `load_json` / `save_json` en `utils.py`. |
| ¿Qué validaciones tienen al crear un pedido? | Negocio existente, productos existentes y disponibles, coordenadas dentro de Medellín, al menos un producto, propina ≥ 0. |
| ¿Qué estados tiene un pedido? | pendiente, preparando, en_camino, entregado, cancelado. Se guarda historial en `status_history`. |
| ¿Cómo generan los datos de prueba? | Con `init_data.py` y `data_generator.py`: negocios, productos por categoría y repartidores con ubicaciones aleatorias en Medellín. |

---

## 6. COMANDOS PARA EJECUTAR EL PROYECTO

```bash
cd backend
pip install -r requirements.txt
```

Desde la raíz del proyecto (donde está `data/`):

```bash
python init_data.py
```

Luego:

```bash
python -m uvicorn backend.app.main:app --reload
```

O desde la raíz con `EJECUTAR.bat` en Windows.  
Abrir: http://localhost:8000 (inicio), http://localhost:8000/delivery (mapa y pedidos), http://localhost:8000/tracking (estado del pedido).

---

*Documento para preparar la sustentación del proyecto ParceroGO.*
