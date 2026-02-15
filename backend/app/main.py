import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_ENV = _PROJECT_ROOT / ".env"
if _ENV.exists():
    from dotenv import load_dotenv
    load_dotenv(_ENV)

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from app.routes import delivery, payments, couriers, notifications, orders

app = FastAPI(
    title="MVP Delivery Local",
    description="Plataforma de delivery para negocios de barrio en Medellín",
    version="1.0.0",
    docs_url=None,
    redoc_url=None
)

_FRONTEND = _PROJECT_ROOT / "frontend"
app.mount("/static", StaticFiles(directory=str(_FRONTEND / "static")), name="static")
templates = Jinja2Templates(directory=str(_FRONTEND / "templates"))

app.include_router(delivery.router, prefix="/api/delivery", tags=["Delivery"])
app.include_router(payments.router, prefix="/api/payments", tags=["Pagos"])
app.include_router(couriers.router, prefix="/api/couriers", tags=["Repartidores"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notificaciones"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])


@app.exception_handler(UnicodeEncodeError)
def unicode_encode_error_handler(request: Request, exc: UnicodeEncodeError):
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor. Intenta de nuevo."},
    )


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/onboarding", response_class=HTMLResponse)
async def onboarding_page(request: Request):
    return templates.TemplateResponse("onboarding.html", {"request": request})


@app.get("/delivery", response_class=HTMLResponse)
async def delivery_page(request: Request):
    return templates.TemplateResponse("delivery.html", {"request": request})


@app.get("/checkout", response_class=HTMLResponse)
async def checkout_page(request: Request):
    return templates.TemplateResponse("checkout.html", {"request": request})


@app.get("/repartidor", response_class=HTMLResponse)
async def repartidor_page(request: Request):
    return templates.TemplateResponse("repartidor.html", {"request": request})


@app.get("/perfil", response_class=HTMLResponse)
async def perfil_page(request: Request):
    return templates.TemplateResponse("perfil.html", {"request": request})


@app.get("/tracking", response_class=HTMLResponse)
async def tracking_page(request: Request):
    return templates.TemplateResponse("tracking.html", {"request": request})


@app.get("/order", response_class=HTMLResponse)
async def order_page(request: Request):
    return templates.TemplateResponse("order.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
