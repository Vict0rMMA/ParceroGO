"""
Módulo de scraping para obtener datos de negocios locales de Medellín

Este módulo genera datos simulados de negocios basados en la estructura
de datos públicos. En un entorno de producción, estos datos se obtendrían
mediante web scraping de directorios públicos de negocios locales.

Nota: Los datos generados son para propósitos académicos y de demostración.
"""

import json
import random
from typing import List, Dict

# Coordenadas geográficas de barrios principales de Medellín, Colombia
MEDELLIN_LOCATIONS = [
    {"name": "El Poblado", "lat": 6.2088, "lng": -75.5704},
    {"name": "Laureles", "lat": 6.2500, "lng": -75.6000},
    {"name": "Envigado", "lat": 6.1699, "lng": -75.5783},
    {"name": "Bello", "lat": 6.3373, "lng": -75.5579},
    {"name": "Itagüí", "lat": 6.1846, "lng": -75.5991},
    {"name": "Sabaneta", "lat": 6.1515, "lng": -75.6167},
    {"name": "Centro", "lat": 6.2476, "lng": -75.5658},
    {"name": "Robledo", "lat": 6.2800, "lng": -75.6000},
]

# Categorías de negocios locales comunes en Medellín
BUSINESS_CATEGORIES = [
    "Restaurante",
    "Comidas Rápidas",
    "Pizzería",
    "Tienda de Abarrotes",
    "Farmacia",
    "Panadería",
    "Supermercado",
    "Cafetería",
    "Veterinaria",
    "Tienda de Mascotas",
]


def scrape_businesses() -> List[Dict]:
    """
    Genera datos de negocios locales de Medellín
    
    Esta función crea una lista de negocios simulados con información
    realista incluyendo ubicación geográfica, categoría y datos de contacto.
    
    En un entorno de producción, esta función realizaría web scraping
    de directorios públicos de negocios locales.
    
    Returns:
        Lista de diccionarios, cada uno representando un negocio con:
        - id, name, category, address, latitude, longitude
        - phone, rating, is_open, delivery_time
    """
    businesses = []
    
    # Mapeo de nombres de negocios a sus categorías correctas
    business_categories_map = {
        # Supermercados
        "Supermercado El Ahorro": "Supermercado",
        "Supermercado El Éxito Local": "Supermercado",
        
        # Restaurantes
        "Restaurante Doña María": "Restaurante",
        "Restaurante La Casona": "Restaurante",
        
        # Farmacias
        "Farmacia La Salud": "Farmacia",
        "Farmacia San Rafael": "Farmacia",
        
        # Panaderías
        "Panadería San José": "Panadería",
        "Panadería La Tradición": "Panadería",
        
        # Cafeterías
        "Café del Barrio": "Cafetería",
        "Cafetería El Buen Sabor": "Cafetería",
        
        # Tiendas de Abarrotes
        "Tienda Don Juan": "Tienda de Abarrotes",
        "Abarrotes La Esquina": "Tienda de Abarrotes",
        "Tienda El Vecino": "Tienda de Abarrotes",
        
        # Veterinarias
        "Veterinaria Mascotas Felices": "Veterinaria",
        "Veterinaria Patitas": "Veterinaria",
        
        # Comidas Rápidas - Hamburguesas
        "Burger King Express": "Comidas Rápidas",
        "McDonald's Delivery": "Comidas Rápidas",
        
        # Comidas Rápidas - Pollo
        "KFC Express": "Comidas Rápidas",
        
        # Pizzerías (categoría especial)
        "Pizza Hut Express": "Pizzería",
        "Domino's Pizza": "Pizzería",
        "Papa John's": "Pizzería",
        
        # Comidas Rápidas - Otros
        "Subway": "Comidas Rápidas",
        "Taco Bell": "Comidas Rápidas",
    }
    
    business_names = [
        "Supermercado El Ahorro",
        "Restaurante Doña María",
        "Farmacia La Salud",
        "Panadería San José",
        "Café del Barrio",
        "Tienda Don Juan",
        "Veterinaria Mascotas Felices",
        "Abarrotes La Esquina",
        "Supermercado El Éxito Local",
        "Restaurante La Casona",
        "Farmacia San Rafael",
        "Panadería La Tradición",
        "Cafetería El Buen Sabor",
        "Tienda El Vecino",
        "Veterinaria Patitas",
        "Burger King Express",
        "McDonald's Delivery",
        "KFC Express",
        "Pizza Hut Express",
        "Domino's Pizza",
        "Subway",
        "Taco Bell",
        "Papa John's",
    ]
    
    for i, name in enumerate(business_names):
        location = random.choice(MEDELLIN_LOCATIONS)
        # Agregar pequeña variación a las coordenadas para simular ubicaciones reales
        lat = location["lat"] + random.uniform(-0.01, 0.01)
        lng = location["lng"] + random.uniform(-0.01, 0.01)
        
        # Obtener categoría del mapa o usar una por defecto
        category = business_categories_map.get(name, random.choice(BUSINESS_CATEGORIES))
        
        business = {
            "id": i + 1,
            "name": name,
            "category": category,
            "address": f"Calle {random.randint(1, 100)} #{random.randint(1, 100)}-{random.randint(1, 100)}, {location['name']}",
            "latitude": round(lat, 6),
            "longitude": round(lng, 6),
            "phone": f"+57 300 {random.randint(1000000, 9999999)}",
            "rating": round(random.uniform(3.5, 5.0), 1),
            "is_open": random.choice([True, True, True, False]),  # 75% probabilidad abierto
            "delivery_time": random.randint(15, 45),  # minutos estimados
        }
        businesses.append(business)
    
    return businesses


def save_businesses() -> List[Dict]:
    """
    Genera y guarda los datos de negocios en un archivo JSON
    
    Returns:
        Lista de negocios generados
    """
    businesses = scrape_businesses()
    with open("data/businesses.json", "w", encoding="utf-8") as f:
        json.dump(businesses, f, indent=2, ensure_ascii=False)
    print(f"Guardados {len(businesses)} negocios en data/businesses.json")
    return businesses


if __name__ == "__main__":
    save_businesses()
