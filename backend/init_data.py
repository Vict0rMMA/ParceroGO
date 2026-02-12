import json
import sys
from pathlib import Path

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT / "backend"))

from app.data_generator import (
    generate_businesses,
    generate_products,
    generate_couriers,
)


def init_all_data():
    data_dir = _PROJECT_ROOT / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    print("[1/4] Generando negocios...")
    businesses = generate_businesses()
    with open(data_dir / "businesses.json", "w", encoding="utf-8") as f:
        json.dump(businesses, f, indent=2, ensure_ascii=False)
    print(f"  Guardados {len(businesses)} negocios.")

    print("\n[2/4] Generando productos locales...")
    products = generate_products(businesses)
    with open(data_dir / "products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    print(f"  Guardados {len(products)} productos.")

    print("\n[3/4] Generando repartidores...")
    couriers = generate_couriers()
    with open(data_dir / "couriers.json", "w", encoding="utf-8") as f:
        json.dump(couriers, f, indent=2, ensure_ascii=False)
    print(f"  Guardados {len(couriers)} repartidores.")

    print("\n[4/4] Archivos de órdenes y pagos...")
    for filename, default_data in [("orders.json", []), ("payments.json", [])]:
        filepath = data_dir / filename
        if not filepath.exists():
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(default_data, f, indent=2, ensure_ascii=False)
            print(f"  Creado {filename}")

    print("\n[COMPLETADO] Datos inicializados.")
    print("\nPara iniciar el servidor (desde la raíz del proyecto):")
    print("  python -m uvicorn backend.app.main:app --reload")


if __name__ == "__main__":
    init_all_data()
