"""
Generación de datos para el proyecto (sin web scraping).
Reemplaza el uso de app.scraping para evitar consumo alto de RAM.
Solo usa memoria local y librería estándar (json, random).
"""

import json
import random
from typing import List, Dict

# -----------------------------------------------------------------------------
# Negocios
# -----------------------------------------------------------------------------
MEDELLIN_LOCATIONS = [
    {"name": "El Poblado", "lat": 6.2088, "lng": -75.5704},
    {"name": "Laureles", "lat": 6.2500, "lng": -75.6000},
    {"name": "Envigado", "lat": 6.1699, "lng": -75.5783},
    {"name": "Bello", "lat": 6.3373, "lng": -75.5579},
    {"name": "Centro", "lat": 6.2476, "lng": -75.5658},
    {"name": "Robledo", "lat": 6.2800, "lng": -75.6000},
]

BUSINESS_NAMES = [
    ("Supermercado El Ahorro", "Supermercado"),
    ("Restaurante Doña María", "Restaurante"),
    ("Farmacia La Salud", "Farmacia"),
    ("Panadería San José", "Panadería"),
    ("Café del Barrio", "Cafetería"),
    ("Tienda Don Juan", "Tienda de Abarrotes"),
    ("Supermercado El Éxito Local", "Supermercado"),
    ("Restaurante La Casona", "Restaurante"),
    ("Farmacia San Rafael", "Farmacia"),
    ("Panadería La Tradición", "Panadería"),
    ("Pizza Hut Express", "Pizzería"),
    ("Domino's Pizza", "Pizzería"),
    ("Burger King Express", "Comidas Rápidas"),
    ("McDonald's Delivery", "Comidas Rápidas"),
    ("Subway", "Comidas Rápidas"),
]

def generate_businesses() -> List[Dict]:
    """Genera lista de negocios (misma estructura que antes)."""
    businesses = []
    for i, (name, category) in enumerate(BUSINESS_NAMES):
        loc = random.choice(MEDELLIN_LOCATIONS)
        lat = loc["lat"] + random.uniform(-0.01, 0.01)
        lng = loc["lng"] + random.uniform(-0.01, 0.01)
        businesses.append({
            "id": i + 1,
            "name": name,
            "category": category,
            "address": f"Calle {random.randint(1, 100)} #{random.randint(1, 100)}-{random.randint(1, 100)}, {loc['name']}",
            "latitude": round(lat, 6),
            "longitude": round(lng, 6),
            "phone": f"+57 300 {random.randint(1000000, 9999999)}",
            "rating": round(random.uniform(3.5, 5.0), 1),
            "is_open": random.choice([True, True, True, False]),
            "delivery_time": random.randint(15, 45),
        })
    return businesses


# -----------------------------------------------------------------------------
# Productos por categoría (muestra reducida)
# -----------------------------------------------------------------------------
# Imágenes Unsplash por producto (relacionadas al nombre: leche, queso, pizza, etc.)
_U = "https://images.unsplash.com/photo-"
_UP = _U + "{}?w=400&h=300&fit=crop"

PRODUCTS_BY_CATEGORY = {
    "Restaurante": [
        {"name": "Bandeja Paisa", "price": 25000, "description": "Plato típico", "image": _UP.format("1546069901-ba9599a7e63c")},
        {"name": "Sancocho", "price": 18000, "description": "Sopa tradicional", "image": _UP.format("1547592166-23ac45744acd")},
        {"name": "Hamburguesa", "price": 15000, "description": "Artesanal", "image": _UP.format("1568901346375-23c9450c58cd")},
    ],
    "Comidas Rápidas": [
        {"name": "Hamburguesa Clásica", "price": 12000, "description": "Con papas", "image": _UP.format("1568901346375-23c9450c58cd")},
        {"name": "Perro Caliente", "price": 8000, "description": "Especial", "image": _UP.format("1619740452663-6b4b8723c6b3")},
        {"name": "Empanadas", "price": 3000, "description": "De carne", "image": _UP.format("1626700051175-6818013e1d4f")},
    ],
    "Pizzería": [
        {"name": "Pizza Margherita", "price": 18000, "description": "Clásica", "image": _UP.format("1513104890138-7c749659a591")},
        {"name": "Pizza Pepperoni", "price": 22000, "description": "Con queso", "image": _UP.format("1628840042765-356cda07504e")},
        {"name": "Pizza Familiar", "price": 35000, "description": "Para compartir", "image": _UP.format("1565299624946-b28f40a0ae38")},
    ],
    "Tienda de Abarrotes": [
        {"name": "Arroz 1kg", "price": 3500, "description": "Arroz premium", "image": _UP.format("1586201375761-83865001e31c")},
        {"name": "Aceite 1L", "price": 8500, "description": "Aceite de cocina", "image": _UP.format("1474979266404-7eaacbcd87c5")},
        {"name": "Azúcar 1kg", "price": 2800, "description": "Azúcar blanca", "image": _UP.format("1587049352846-4a222e784d38")},
    ],
    "Farmacia": [
        {"name": "Acetaminofén", "price": 5000, "description": "500mg", "image": _UP.format("1584308666744-24d5c474f2ae")},
        {"name": "Ibuprofeno", "price": 6000, "description": "Antiinflamatorio", "image": _UP.format("1584308666744-24d5c474f2ae")},
        {"name": "Alcohol", "price": 3500, "description": "500ml", "image": _UP.format("1584308666744-24d5c474f2ae")},
    ],
    "Panadería": [
        {"name": "Pan de Bono", "price": 500, "description": "Tradicional", "image": _UP.format("1509440159596-0249088772ff")},
        {"name": "Almojábana", "price": 600, "description": "Fresca", "image": _UP.format("1509440159596-0249088772ff")},
        {"name": "Pan Integral", "price": 3000, "description": "500g", "image": _UP.format("1558961363-fa8fdf82db35")},
    ],
    "Supermercado": [
        {"name": "Leche 1L", "price": 4500, "description": "Entera", "image": _UP.format("1563636619-914057cff423")},
        {"name": "Huevos x12", "price": 8000, "description": "AA", "image": _UP.format("1582722872445-44dc5f7e3c8f")},
        {"name": "Queso 250g", "price": 5500, "description": "Campesino", "image": _UP.format("1486297678162-eb2a19b0a32d")},
    ],
    "Cafetería": [
        {"name": "Café Tinto", "price": 2000, "description": "Colombiano", "image": _UP.format("1517487881594-2787fef5ebf7")},
        {"name": "Cappuccino", "price": 4500, "description": "Italiano", "image": _UP.format("1572442388796-11668a67e53d")},
        {"name": "Pastel", "price": 4000, "description": "Casero", "image": _UP.format("1578985545062-69928b1d9587")},
    ],
}

DEFAULT_PRODUCTS = list(PRODUCTS_BY_CATEGORY["Tienda de Abarrotes"])


def generate_products(businesses: List[Dict]) -> List[Dict]:
    """Genera productos por negocio (misma estructura que antes)."""
    products = []
    pid = 1
    for b in businesses:
        cat = b["category"]
        templates = PRODUCTS_BY_CATEGORY.get(cat, DEFAULT_PRODUCTS)
        n = min(random.randint(3, 5), len(templates))
        for t in random.sample(templates, n):
            products.append({
                "id": pid,
                "business_id": b["id"],
                "name": t["name"],
                "price": t["price"],
                "description": t["description"],
                "category": cat,
                "available": random.choice([True, True, True, False]),
                "image": t.get("image", "https://picsum.photos/seed/0/400"),
            })
            pid += 1
    return products


# -----------------------------------------------------------------------------
# Repartidores
# -----------------------------------------------------------------------------
COURIER_NAMES = ["Carlos", "María", "Pedro", "Ana", "Luis", "Sofia", "Juan", "Laura"]


def generate_couriers() -> List[Dict]:
    """Genera repartidores (misma estructura que antes)."""
    couriers = []
    for i in range(8):
        loc = random.choice(MEDELLIN_LOCATIONS)
        lat = loc["lat"] + random.uniform(-0.015, 0.015)
        lng = loc["lng"] + random.uniform(-0.015, 0.015)
        couriers.append({
            "id": i + 1,
            "name": COURIER_NAMES[i % len(COURIER_NAMES)],
            "phone": f"+57 300 {1000000 + i}",
            "lat": round(lat, 6),
            "lng": round(lng, 6),
            "zone": loc["name"],
            "available": random.choice([True, True, True, False]),
            "vehicle": random.choice(["Moto", "Bicicleta", "Moto", "Moto"]),
            "rating": round(random.uniform(4.0, 5.0), 1),
            "current_order_id": None,
            "total_deliveries": random.randint(10, 200),
        })
    return couriers


# -----------------------------------------------------------------------------
# Productos Jumbo (estáticos, sin scraping)
# -----------------------------------------------------------------------------
JUMBO_STATIC = [
    ("Refrigeración", "Nevera Samsung 380L", 1899000),
    ("Refrigeración", "Nevecon 210L", 1299000),
    ("Lavadoras", "Lavadora Samsung 9kg", 2499000),
    ("Televisores", "Smart TV Samsung 55\" 4K", 2499000),
    ("Celulares", "Samsung Galaxy A54 128GB", 1299000),
    ("Despensa", "Arroz Diana 1kg", 3500),
    ("Despensa", "Aceite Girasoli 1L", 8500),
    ("Despensa", "Café Juan Valdez 500g", 18900),
    ("Lácteos", "Leche Alpina 1L", 4500),
    ("Lácteos", "Huevos AA x12", 8000),
    ("Frutas y Verduras", "Banano x1kg", 3500),
    ("Frutas y Verduras", "Papa Pastusa x1kg", 3200),
    ("Carnes", "Pechuga de Pollo x1kg", 12900),
    ("Aseo", "Detergente Ariel 1kg", 12900),
    ("Cuidado Personal", "Shampoo Pantene 400ml", 12900),
]


def generate_jumbo_products() -> List[Dict]:
    """Genera productos Jumbo estáticos (sin peticiones HTTP)."""
    out = []
    for i, (category, name, price) in enumerate(JUMBO_STATIC, 1):
        out.append({
            "id": i,
            "name": name,
            "price": price,
            "description": f"Producto de {category} - {name}",
            "category": category,
            "source": "Jumbo Colombia",
            "available": True,
            "image": f"https://picsum.photos/seed/j{i}/400",
        })
    return out
