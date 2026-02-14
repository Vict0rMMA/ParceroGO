# ParceroGO — Guía completa (explicación, ejecución y estudio)

Un solo documento con todo: qué es el proyecto, cómo ejecutarlo, arquitectura POO y preguntas para la sustentación.

---

## 1. ¿Qué es ParceroGO?

- **MVP de delivery local** para negocios de barrio en Medellín.
- El usuario ve un **mapa** (Leaflet + OpenStreetMap), elige negocio, agrega productos al **carrito**, hace el **pedido** (nombre, teléfono, dirección) y puede **pagar** (efectivo o tarjeta, **simulado**) y ver el **estado** en tracking.
- Los **repartidores** tienen panel para asignarse pedidos y marcar “en camino” y “entregado”.
- **Sin base de datos:** todo se guarda en archivos JSON en la carpeta `data/`.
- **Stack:** Backend FastAPI (Python), frontend HTML/CSS/JavaScript vanilla, mapa Leaflet, PWA (Service Worker + manifest).

---

## 2. Cómo ejecutarlo

### Paso 1 — Primera vez (desde la raíz del proyecto)

Abre **PowerShell** o **CMD** y ejecuta:

```powershell
cd "c:\Users\victo\Downloads\ParceroGO-main"
pip install -r backend/requirements.txt
python backend/init_data.py
```

(Eso instala dependencias y crea los datos en `data/`.)

### Paso 2 — Levantar el servidor (desde la carpeta backend)

**Importante:** el servidor se ejecuta desde dentro de `backend`, no desde la raíz:

```powershell
cd "c:\Users\victo\Downloads\ParceroGO-main\backend"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Cuando veas en pantalla: **`Uvicorn running on http://127.0.0.1:8000`**, abre el navegador en:

- **Inicio:** http://127.0.0.1:8000  
- **Delivery (mapa y pedidos):** http://127.0.0.1:8000/delivery  
- **Tracking:** http://127.0.0.1:8000/tracking  
- **Repartidor:** http://127.0.0.1:8000/repartidor  

**Detener el servidor:** en la misma ventana de la terminal presiona **`Ctrl + C`**.

**Si el puerto 8000 está ocupado:** usa otro puerto, por ejemplo `--port 8001`, y abre http://127.0.0.1:8001

---

## 3. Arquitectura y POO

### Stack

- **Backend:** FastAPI (Python), API REST, sirve HTML.
- **Frontend:** HTML, CSS, JavaScript vanilla (ES6+).
- **Mapa:** Leaflet + OpenStreetMap.
- **Datos:** JSON en `data/` (sin BD).
- **PWA:** Service Worker + manifest.

### Estructura del backend (capas)

| Capa | Carpeta | Responsabilidad |
|------|---------|-----------------|
| **Models** | `backend/app/models/` | Order, Product, Business, Courier, Payment (dataclasses, from_dict/to_dict) |
| **Repositories** | `backend/app/repositories/` | Leer/escribir en `data/*.json` (OrderRepository, ProductRepository, etc.) |
| **Services** | `backend/app/services/` | Lógica de negocio: OrderService, PaymentService, CourierService, GeoService (Haversine) |
| **Routes** | `backend/app/routes/` | Recibir HTTP, llamar al servicio, devolver JSON (sin lógica de negocio) |

- **POO backend:** encapsulación (servicios reciben repositorios), composición (OrderService usa varios repos), responsabilidad única (cada capa hace una cosa).
- **POO frontend:** en `frontend/static/delivery-services.js` están las clases **ApiService** (llamadas a la API), **Cart** (carrito) y **MapService** (mapa Leaflet); se exponen en `window.ParceroGO`.
- **PWA:** `frontend/static/sw.js` hace cache-first de estáticos (CSS, JS); la estrategia está comentada en el archivo.

### Flujo de un pedido

1. Usuario en **Delivery** → ve mapa con negocios → elige negocio → agrega productos al carrito.  
2. **Confirmar pedido** → datos del cliente y dirección → backend crea pedido (valida, calcula total y distancia con Haversine, guarda en `orders.json`).  
3. Usuario **paga** (efectivo o tarjeta simulado) → se actualiza `payments.json` y estado del pedido.  
4. En **Tracking** busca por teléfono → ve estado (pendiente → preparando → en camino → entregado).  
5. **Repartidor** en panel asigna pedido y marca “en camino” y luego “entregado”.

---

## 4. Preguntas típicas del profe (y respuestas cortas)

| Pregunta | Respuesta |
|----------|-----------|
| ¿Qué es el proyecto? | MVP de delivery local para Medellín: mapa, carrito, pedidos, pagos y tracking simulados; datos en JSON. |
| ¿Por qué no usan base de datos? | Es un MVP académico; JSON para ir rápido. En producción se usaría una BD. |
| ¿Cómo calculan la distancia? | Fórmula de Haversine en `utils.py` / GeoService (Tierra = esfera 6371 km). |
| ¿Los pagos son reales? | No. Solo se valida formato y se guarda estado en JSON; no hay pasarela de pago. |
| ¿Qué es FastAPI? | Framework de Python para el servidor y las APIs REST. |
| ¿Qué es Leaflet? | Librería JavaScript para mapas; usamos OpenStreetMap centrado en Medellín. |
| ¿Cómo asignan al repartidor? | Por cercanía (Haversine). La asignación se hace en el panel repartidor. |
| ¿Dónde se guardan los pedidos? | En `data/orders.json`; los repositorios leen/escriben con load_json/save_json. |
| ¿Qué validan al crear un pedido? | Negocio existente, productos existentes y disponibles, coordenadas en Medellín, al menos un producto, propina ≥ 0. |
| ¿Estados del pedido? | pendiente, preparando, en_camino, entregado, cancelado. |
| ¿De dónde salen negocios y productos? | Del script `backend/init_data.py` con `data_generator.py` (datos de prueba en Medellín). |

---

## 5. Subir a GitHub

Desde la raíz del proyecto:

```powershell
git add .
git commit -m "Tu mensaje"
git push origin main
```

Si aún no tienes remoto: `git remote add origin https://github.com/TU_USUARIO/ParceroGO.git`

---

## 6. Integrantes

- Victor Manuel Monsalve Aguilar  
- David Velez Pino  
- David Santiago Rodriguez Ruiz  

---

*Documento único de referencia para ParceroGO.*
