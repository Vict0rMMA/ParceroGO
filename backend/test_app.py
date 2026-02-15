import os
import sys

                                  
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def _root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def check_structure():
    root = _root()
    os.chdir(root)
    print("Verificando estructura del proyecto...\n")
    
    required_files = [
        "backend/app/main.py",
        "backend/app/routes/delivery.py",
        "backend/app/routes/payments.py",
        "backend/app/routes/couriers.py",
        "backend/app/routes/orders.py",
        "frontend/templates/index.html",
        "frontend/templates/delivery.html",
        "frontend/static/style.css",
        "frontend/static/delivery.js",
        "backend/requirements.txt",
        "backend/init_data.py"
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"  [OK] {file}")
        else:
            print(f"  [FALTA] {file}")
            missing.append(file)
    
    required_dirs = ["data", "backend", "backend/app", "backend/app/routes", "frontend", "frontend/templates", "frontend/static"]
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"  [OK] directorio: {dir_path}/")
        else:
            print(f"  [FALTA] directorio: {dir_path}/")
            missing.append(dir_path)
    
    if missing:
        print(f"\n[ADVERTENCIA] Faltan {len(missing)} archivos/directorios")
        return False
    else:
        print("\n[OK] Estructura completa")
        return True

def check_data_files():
    root = _root()
    os.chdir(root)
    print("\nVerificando archivos de datos...\n")
    
    data_files = [
        "data/businesses.json",
        "data/products.json",
        "data/couriers.json",
        "data/orders.json",
        "data/payments.json"
    ]
    
    all_exist = True
    for file in data_files:
        if os.path.exists(file):
            if file in ["data/orders.json", "data/payments.json"]:
                print(f"  [OK] {file} (puede estar vacío)")
            else:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content and content != "[]":
                        print(f"  [OK] {file} (con datos)")
                    else:
                        print(f"  [VACÍO] {file} (ejecuta backend/init_data.py)")
                        all_exist = False
        else:
            print(f"  [FALTA] {file}")
            all_exist = False
    
    return all_exist

def check_imports():
    print("\nVerificando imports...\n")
    root = _root()
    try:
        original_dir = os.getcwd()
        sys.path.insert(0, os.path.join(root, "backend"))
        os.chdir(root)
        
        try:
            from app.routes import delivery, payments, couriers, notifications, orders
            print("  [OK] Imports de rutas funcionan")
        except Exception as e:
            print(f"  [ERROR] Error en imports de rutas: {e}")
            return False
        
        try:
            from app.data_generator import generate_businesses
            print("  [OK] Imports de data_generator funcionan")
        except Exception as e:
            print(f"  [ADVERTENCIA] Error en data_generator: {e}")
        
        os.chdir(original_dir)
        return True
        
    except Exception as e:
        print(f"  [ERROR] Error verificando imports: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("  VERIFICACION DE LA APLICACION MVP")
    print("=" * 50)
    print()
    
    structure_ok = check_structure()
    data_ok = check_data_files()
    imports_ok = check_imports()
    
    print("\n" + "=" * 50)
    print("  RESUMEN")
    print("=" * 50)
    
    if structure_ok and imports_ok:
        print("\n[OK] La aplicación está lista para ejecutarse")
        if not data_ok:
            print("\n[IMPORTANTE] Ejecuta 'python backend/init_data.py' para poblar los datos")
        print("\nPara iniciar el servidor (desde la raíz del proyecto):")
        print("   python -m uvicorn backend.app.main:app --reload")
    else:
        print("\n[ERROR] Hay problemas que deben resolverse antes de ejecutar")
    
    print()
