"""
Aplicación principal FastAPI - MVP Delivery Local
Sistema de delivery para negocios de barrio en Medellín, Colombia.
Arquitectura: FastAPI, JSON, HTML/JS, Leaflet.
Autor: Proyecto Académico. Versión: 1.0.0
"""

# -----------------------------------------------------------------------------
# Imports y configuración de entorno
# -----------------------------------------------------------------------------
from pathlib import Path

# Raíz del proyecto (donde están backend/, frontend/, data/)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_ENV = _PROJECT_ROOT / ".env"
if _ENV.exists():
    from dotenv import load_dotenv
    load_dotenv(_ENV)

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from app.routes import delivery, payments, couriers, notifications, orders

# -----------------------------------------------------------------------------
# Inicialización de la aplicación
# -----------------------------------------------------------------------------
app = FastAPI(
    title="MVP Delivery Local",
    description="Plataforma de delivery para negocios de barrio en Medellín",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Frontend: estáticos y plantillas (carpeta frontend/ en la raíz del proyecto)
_FRONTEND = _PROJECT_ROOT / "frontend"
app.mount("/static", StaticFiles(directory=str(_FRONTEND / "static")), name="static")
templates = Jinja2Templates(directory=str(_FRONTEND / "templates"))

# -----------------------------------------------------------------------------
# Registro de rutas (API y páginas)
# -----------------------------------------------------------------------------
app.include_router(delivery.router, prefix="/api/delivery", tags=["Delivery"])
app.include_router(payments.router, prefix="/api/payments", tags=["Pagos"])
app.include_router(couriers.router, prefix="/api/couriers", tags=["Repartidores"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notificaciones"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])

# -----------------------------------------------------------------------------
# Rutas de páginas HTML (vistas principales)
# -----------------------------------------------------------------------------


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Página principal: mapa de Medellín con negocios locales."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/onboarding", response_class=HTMLResponse)
async def onboarding_page(request: Request):
    """Pantalla de bienvenida / onboarding (simulada, sin auth real)."""
    return templates.TemplateResponse("onboarding.html", {"request": request})


@app.get("/delivery", response_class=HTMLResponse)
async def delivery_page(request: Request):
    """Página de delivery: negocios, productos y creación de pedidos."""
    return templates.TemplateResponse("delivery.html", {"request": request})


@app.get("/jumbo", response_class=HTMLResponse)
async def jumbo_page(request: Request):
    """Página de productos Jumbo (scraping)."""
    return templates.TemplateResponse("jumbo.html", {"request": request})


@app.get("/checkout", response_class=HTMLResponse)
async def checkout_page(request: Request):
    """Página de checkout para procesar pagos."""
    return templates.TemplateResponse("checkout.html", {"request": request})


@app.get("/repartidor", response_class=HTMLResponse)
async def repartidor_page(request: Request):
    """Vista repartidor: pedidos asignados y marcar entregado."""
    return templates.TemplateResponse("repartidor.html", {"request": request})


@app.get("/panel", response_class=HTMLResponse)
async def panel_page(request: Request):
    """Panel del negocio: ver pedidos y cambiar estado."""
    return templates.TemplateResponse("panel.html", {"request": request})


@app.get("/perfil", response_class=HTMLResponse)
async def perfil_page(request: Request):
    """Perfil de usuario: datos, direcciones, historial."""
    return templates.TemplateResponse("perfil.html", {"request": request})


@app.get("/tracking", response_class=HTMLResponse)
async def tracking_page(request: Request):
    """Página de seguimiento de pedidos por teléfono o ID."""
    return templates.TemplateResponse("tracking.html", {"request": request})


@app.get("/order", response_class=HTMLResponse)
async def order_page(request: Request):
    """Página de confirmación de pedido (carrito desde sessionStorage)."""
    return templates.TemplateResponse("order.html", {"request": request})


# -----------------------------------------------------------------------------
# Punto de entrada (servidor de desarrollo)
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
