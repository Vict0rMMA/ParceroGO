"""
Utilidades compartidas para el proyecto MVP Delivery.
Incluye: carga/guardado JSON, cálculo de distancia (Haversine), timestamps y validación de coordenadas.
"""

import json
import math
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict

# -----------------------------------------------------------------------------
# Configuración (data/ en la raíz del proyecto)
# -----------------------------------------------------------------------------
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = str(_PROJECT_ROOT / "data")

# -----------------------------------------------------------------------------
# Persistencia JSON
# -----------------------------------------------------------------------------


def load_json(file_name: str) -> List[Dict]:
    """
    Carga datos desde un archivo JSON en el directorio data/.
    Si el archivo no existe o hay error de lectura, retorna lista vacía.
    """
    file_path = os.path.join(DATA_DIR, file_name)
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_json(file_name: str, data: List[Dict]) -> None:
    """
    Guarda una lista de diccionarios en un archivo JSON en data/.
    Crea el directorio si no existe. Usa indent=2 y ensure_ascii=False.
    """
    file_path = os.path.join(DATA_DIR, file_name)
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# -----------------------------------------------------------------------------
# Geografía y tiempo
# -----------------------------------------------------------------------------


def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    Calcula la distancia en kilómetros entre dos puntos geográficos (fórmula de Haversine).
    """
    R = 6371  # Radio de la Tierra en km
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))
    return R * c


def get_current_timestamp() -> str:
    """Retorna la fecha y hora actual en formato ISO 8601."""
    return datetime.now().isoformat()


def validate_coordinates(lat: float, lng: float) -> bool:
    """
    Valida que las coordenadas estén dentro de rangos válidos para Medellín y área metropolitana.
    """
    MEDELLIN_LAT_RANGE = (6.0, 6.5)
    MEDELLIN_LNG_RANGE = (-75.8, -75.4)
    return (
        MEDELLIN_LAT_RANGE[0] <= lat <= MEDELLIN_LAT_RANGE[1]
        and MEDELLIN_LNG_RANGE[0] <= lng <= MEDELLIN_LNG_RANGE[1]
    )
