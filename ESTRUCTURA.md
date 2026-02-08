# Estructura del proyecto – MVP Delivery Local

El proyecto está organizado en carpetas claras: **backend**, **frontend** y **data**.

---

## Vista general

```
DELIVERY-main/
├── backend/          ← Backend (Python, FastAPI, API)
├── frontend/         ← Frontend (HTML, CSS, JS)
├── data/             ← Datos (JSON)
├── ESTRUCTURA.md     ← Este archivo
├── EJECUTAR.bat      ← Iniciar servidor (Windows)
└── *.md              ← Documentación
```

---

## Backend (`backend/`)

Todo el servidor y la lógica de la API.

| Qué | Dónde |
|-----|--------|
| App FastAPI | `backend/app/main.py` |
| Rutas API | `backend/app/routes/` (delivery, payments, couriers, orders, notifications) |
| Utilidades | `backend/app/utils.py` (JSON, distancia, etc.) |
| Generación de datos | `backend/app/data_generator.py` |
| SMS / notificaciones | `backend/app/notify_sms.py`, `backend/app/sms_service.py` |
| Inicializar datos | `backend/init_data.py` |
| Dependencias | `backend/requirements.txt` |
| Tests | `backend/test_app.py`, `backend/test_notification.py` |

**Cómo ejecutar el servidor** (desde la raíz del proyecto):

```bash
python -m uvicorn backend.app.main:app --reload
```

**Cómo generar datos** (desde la raíz):

```bash
python backend/init_data.py
```

---

## Frontend (`frontend/`)

Páginas, estilos y scripts del navegador.

| Qué | Dónde |
|-----|--------|
| Plantillas HTML | `frontend/templates/` (index, delivery, checkout, tracking, perfil, etc.) |
| CSS | `frontend/static/style.css` |
| JavaScript | `frontend/static/` (delivery.js, address.js, theme.js, alerts.js) |
| PWA | `frontend/static/manifest.json`, `frontend/static/sw.js` |

El backend sirve todo esto desde `frontend/templates` y `frontend/static`.

---

## Data (`data/`)

Archivos JSON en la raíz del proyecto (no dentro de backend).

- `businesses.json` – Negocios  
- `products.json` – Productos por negocio  
- `couriers.json` – Repartidores  
- `orders.json` – Pedidos  
- `payments.json` – Pagos  
- `config.json` – Configuración (SMS, etc.)

---

## Resumen

| Parte | Carpeta | Contenido |
|-------|---------|-----------|
| **Backend** | `backend/` | Python, FastAPI, API, init_data, tests |
| **Frontend** | `frontend/` | templates + static (HTML, CSS, JS) |
| **Data** | `data/` | JSON (negocios, pedidos, etc.) |
| **Docs** | Raíz `*.md` | README, ESTRUCTURA, EJECUTAR, etc. |

Siempre ejecuta los comandos **desde la raíz del proyecto** (donde están las carpetas `backend/`, `frontend/` y `data/`).
