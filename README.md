# ParceroGo — MVP Delivery Local

> Plataforma de delivery para negocios de barrio en Medellín, Colombia.  
> Proyecto académico con FastAPI, mapa interactivo y pagos simulados.

**Guía completa (cómo ejecutar, arquitectura, estudio):** ver **[GUIA-PARCEROGO.md](GUIA-PARCEROGO.md)**.

---

## Características

| Componente | Descripción |
|------------|-------------|
| Mapa interactivo | Negocios y repartidores con Leaflet + OpenStreetMap |
| Catálogo | Productos por negocio (datos simulados) |
| Pagos | Efectivo y tarjeta (simulado, sin pasarelas reales) |
| Repartidores | Asignación por cercanía |
| Sin BD | Todo en JSON y memoria |
| Sesión | Login/cierre de sesión simulados en el frontend |

---

## Instalación

**Requisitos:** Python 3.8+

```bash
# 1. Ir a la carpeta del backend
cd backend

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Generar datos iniciales (negocios, productos, repartidores)
python init_data.py

# 4. Levantar el servidor
python -m uvicorn app.main:app --reload
```

**Acceso:**

- Inicio: http://localhost:8000  
- Delivery: http://localhost:8000/delivery  
- API Docs: http://localhost:8000/api/docs (si están habilitadas en `main.py`).  

En Windows puedes usar **`EJECUTAR.bat`** desde la raíz del proyecto (abre la terminal, va a `backend/`, instala dependencias si hace falta y levanta el servidor).

---

## Configuración opcional (.env)

- **`.env`** y **`.env.example`** son para configurar **Twilio** (SMS reales). **No son necesarios** para usar la app: los SMS y pagos son simulados.
- Si más adelante quieres enviar SMS reales: copia `.env.example` a `.env` y completa `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` y `TWILIO_PHONE`. No subas `.env` a Git (ya está en `.gitignore`).
- **`.gitignore`** debe quedarse: evita subir claves y archivos innecesarios.

---

## Estructura del proyecto

```
ParceroGO-main/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI, rutas HTML y API
│   │   ├── utils.py          # JSON, distancia, coordenadas
│   │   ├── data_generator.py
│   │   ├── notify_sms.py
│   │   ├── sms_service.py
│   │   └── routes/          # delivery, payments, couriers, orders, notifications
│   ├── init_data.py         # Pobla data/*.json
│   └── requirements.txt
├── frontend/
│   ├── static/              # CSS, JS, imágenes, manifest, sw
│   └── templates/           # HTML (index, delivery, checkout, tracking, panel, etc.)
├── data/                    # businesses.json, products.json, couriers.json, orders.json, payments.json, config.json
├── scripts/                 # build-vercel.js (despliegue estático)
├── .env.example
├── .gitignore
├── EJECUTAR.bat             # Iniciar servidor (Windows)
├── ESTRUCTURA.md            # Estructura detallada y limpieza del proyecto
└── README.md
```

---

## API principal

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/delivery/businesses` | Lista negocios |
| GET | `/api/delivery/businesses/{id}/products` | Productos de un negocio |
| POST | `/api/delivery/orders` | Crear pedido |
| PATCH | `/api/delivery/orders/{id}/status` | Cambiar estado del pedido |
| POST | `/api/payments/process` | Procesar pago simulado |
| GET | `/api/couriers/available` | Repartidores disponibles |

Más rutas en http://localhost:8000/api/docs .

---

## Mapa

- **Leaflet.js** + **OpenStreetMap** (tiles CartoDB).
- Centro: Medellín (6.2476° N, 75.5658° W).
- Negocios y repartidores como marcadores; distancias con Haversine.

---

## Tecnologías

- **Backend:** FastAPI (Python)
- **Frontend:** HTML, CSS, JavaScript (vanilla)
- **Mapa:** Leaflet.js, OpenStreetMap
- **Datos:** JSON (sin base de datos)

---

## Aviso

- Pagos y SMS son **simulados** (no hay transacciones ni envíos reales).
- Datos de negocios y productos son de demostración/académicos.

---

## Repositorio Git

El proyecto ya está inicializado con Git (rama `main`). Para subirlo a GitHub:

1. Crea un repo vacío en GitHub (sin README).
2. En la carpeta del proyecto:

```bash
git remote add origin https://github.com/TU_USUARIO/ParceroGO.git
git push -u origin main
```

(Si `origin` ya existe: `git remote set-url origin https://github.com/TU_USUARIO/ParceroGO.git`)

---

## Integrantes

- **Victor Manuel Monsalve Aguilar**
- **David Velez Pino**
- **David Santiago Rodriguez Ruiz**


