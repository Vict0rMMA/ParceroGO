"""
Script para inicializar todos los datos del proyecto (sin web scraping).
Ejecutar desde la raíz del proyecto: python backend/init_data.py

Genera: data/businesses.json, products.json, jumbo_products.json, couriers.json;
crea orders.json y payments.json vacíos si no existen.
"""

import json
import os
import sys
from pathlib import Path

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Raíz del proyecto (donde están backend/, frontend/, data/)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT / "backend"))

from app.data_generator import (
    generate_businesses,
    generate_products,
    generate_couriers,
    generate_jumbo_products,
)


def init_all_data():
    """Genera todos los datos y escribe los JSON en data/."""
    data_dir = _PROJECT_ROOT / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    print("Inicializando datos del proyecto (sin scraping)...\n")

    print("[1/5] Generando negocios...")
    businesses = generate_businesses()
    with open(data_dir / "businesses.json", "w", encoding="utf-8") as f:
        json.dump(businesses, f, indent=2, ensure_ascii=False)
    print(f"  Guardados {len(businesses)} negocios.")

    print("\n[2/5] Generando productos locales...")
    products = generate_products(businesses)
    with open(data_dir / "products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    print(f"  Guardados {len(products)} productos.")

    print("\n[3/5] Generando productos Jumbo (estáticos)...")
    jumbo_products = generate_jumbo_products()
    with open(data_dir / "jumbo_products.json", "w", encoding="utf-8") as f:
        json.dump(jumbo_products, f, indent=2, ensure_ascii=False)
    print(f"  Guardados {len(jumbo_products)} productos Jumbo.")

    print("\n[4/5] Generando repartidores...")
    couriers = generate_couriers()
    with open(data_dir / "couriers.json", "w", encoding="utf-8") as f:
        json.dump(couriers, f, indent=2, ensure_ascii=False)
    print(f"  Guardados {len(couriers)} repartidores.")

    print("\n[5/5] Archivos de órdenes y pagos...")
    for filename, default_data in [("orders.json", []), ("payments.json", [])]:
        filepath = data_dir / filename
        if not filepath.exists():
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(default_data, f, indent=2, ensure_ascii=False)
            print(f"  Creado {filename}")

    print("\n[COMPLETADO] Datos inicializados (sin scraping).")
    print("\nPara iniciar el servidor (desde la raíz del proyecto):")
    print("  python -m uvicorn backend.app.main:app --reload")


if __name__ == "__main__":
    init_all_data()
