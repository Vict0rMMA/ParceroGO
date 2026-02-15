from fastapi import APIRouter, HTTPException
from typing import Optional

from app.repositories.business_repository import BusinessRepository
from app.repositories.product_repository import ProductRepository
from app.services.order_service import OrderService

router = APIRouter()

_order_service = OrderService()
_business_repo = BusinessRepository()
_product_repo = ProductRepository()


@router.get("/businesses")
async def get_businesses():
    businesses = _business_repo.find_all()
    return {"businesses": businesses}


@router.get("/businesses/{business_id}")
async def get_business(business_id: int):
    business = _business_repo.find_by_id(business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    return business


@router.get("/businesses/{business_id}/products")
async def get_business_products(business_id: int):
    products = _product_repo.find_by_business_id(business_id, only_available=True)
    return {"products": products}


@router.get("/products")
async def get_all_products(category: Optional[str] = None):
    all_products = _product_repo.find_all()
    if category:
        all_products = [p for p in all_products if p.get("category", "").lower() == category.lower()]
    return {"products": all_products, "count": len(all_products), "category": category}


@router.post("/orders")
async def create_order(order_data: dict):
    try:
        return _order_service.create_order(order_data)
    except ValueError as e:
        msg = str(e)
        if "no encontrado" in msg.lower():
            raise HTTPException(status_code=404, detail=msg)
        raise HTTPException(status_code=400, detail=msg)


@router.get("/orders")
async def get_orders(courier_id: Optional[int] = None, business_id: Optional[int] = None):
    return _order_service.get_orders(courier_id=courier_id, business_id=business_id)


@router.get("/orders/by-phone/{phone}")
async def get_orders_by_phone(phone: str):
    return _order_service.get_orders_by_phone(phone)


@router.get("/orders/{order_id}")
async def get_order(order_id: int):
    order = _order_service.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return {"order": order}


@router.patch("/orders/{order_id}/status")
async def update_order_status(order_id: int, status_data: dict):
    try:
        return _order_service.update_status(order_id, status_data)
    except ValueError as e:
        if "no encontrado" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/delivery-persons")
async def get_delivery_persons():
    from app.repositories.courier_repository import CourierRepository
    couriers = CourierRepository().find_all()
    return {"delivery_persons": couriers}


@router.get("/cart")
async def get_cart():
    return {"items": [], "total": 0, "item_count": 0}


@router.post("/cart/add")
async def add_to_cart(cart_item: dict):
    product = _product_repo.find_by_id(cart_item["product_id"])
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if not product.get("available", True):
        raise HTTPException(status_code=400, detail=f"Producto {product['name']} no disponible")
    quantity = cart_item.get("quantity", 1)
    return {
        "success": True,
        "product": {
            "id": product["id"],
            "name": product["name"],
            "price": product["price"],
            "image": product.get("image", ""),
            "category": product.get("category", ""),
            "quantity": quantity,
            "subtotal": product["price"] * quantity,
        },
        "message": f"{product['name']} agregado al carrito",
    }


@router.delete("/cart/remove/{product_id}")
async def remove_from_cart(product_id: int):
    product = _product_repo.find_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {
        "success": True,
        "product_id": product_id,
        "message": f"{product['name']} removido del carrito",
    }
