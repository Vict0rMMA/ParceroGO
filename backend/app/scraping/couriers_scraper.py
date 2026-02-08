"""
Módulo de generación de datos de repartidores simulados

Genera datos de repartidores con ubicaciones en Medellín
para simular el sistema de entrega.
"""

import json
import random
from typing import List, Dict

# Coordenadas geográficas de barrios principales de Medellín
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

COURIER_NAMES = [
    "Carlos", "María", "Pedro", "Ana", "Luis", "Sofia",
    "Juan", "Laura", "Diego", "Camila", "Andrés", "Valentina"
]


def generate_couriers() -> List[Dict]:
    """
    Genera datos de repartidores simulados
    
    Returns:
        Lista de diccionarios con información de repartidores
    """
    couriers = []
    
    # Generar 8 repartidores distribuidos en diferentes zonas
    for i in range(8):
        location = random.choice(MEDELLIN_LOCATIONS)
        # Agregar variación a las coordenadas
        lat = location["lat"] + random.uniform(-0.015, 0.015)
        lng = location["lng"] + random.uniform(-0.015, 0.015)
        
        courier = {
            "id": i + 1,
            "name": COURIER_NAMES[i % len(COURIER_NAMES)],
            "phone": f"+57 300 {1000000 + i}",
            "lat": round(lat, 6),
            "lng": round(lng, 6),
            "zone": location["name"],
            "available": random.choice([True, True, True, False]),  # 75% disponibles
            "vehicle": random.choice(["Moto", "Bicicleta", "Moto", "Moto"]),  # Mayoría en moto
            "rating": round(random.uniform(4.0, 5.0), 1),
            "current_order_id": None,
            "total_deliveries": random.randint(10, 200)
        }
        couriers.append(courier)
    
    return couriers


def save_couriers() -> List[Dict]:
    """
    Genera y guarda los datos de repartidores en un archivo JSON
    
    Returns:
        Lista de repartidores generados
    """
    couriers = generate_couriers()
    with open("data/couriers.json", "w", encoding="utf-8") as f:
        json.dump(couriers, f, indent=2, ensure_ascii=False)
    print(f"Guardados {len(couriers)} repartidores en data/couriers.json")
    return couriers


if __name__ == "__main__":
    save_couriers()
