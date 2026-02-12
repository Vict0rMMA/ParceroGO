"""
Script para actualizar las URLs de imágenes de productos de Jumbo

Uso:
    python update_jumbo_images.py
    
    Luego ingresa las URLs de las imágenes cuando se te solicite,
    o pásalas como argumentos en formato JSON.
"""

import json
import os
import sys

# Configurar encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def update_jumbo_images(image_urls: dict = None):
    """
    Actualiza las URLs de imágenes de productos de Jumbo
    
    Args:
        image_urls: Diccionario con {product_id: image_url} o {product_name: image_url}
    """
    json_path = "data/jumbo_products.json"
    
    # Cargar productos actuales
    if not os.path.exists(json_path):
        print(f"❌ Error: No se encontró el archivo {json_path}")
        print("   Ejecuta primero: python init_data.py")
        return
    
    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    print(f"📦 Productos encontrados: {len(products)}")
    
    # Si no se proporcionaron URLs, pedirlas al usuario
    if not image_urls:
        print("\n📸 Ingresa las URLs de las imágenes de Jumbo")
        print("   Formato: ID o Nombre del producto = URL")
        print("   Ejemplo: 1 = https://jumbocolombia.vteximg.com.br/arquivos/ids/123456")
        print("   O: 'Nevera Samsung RT38K5932S8 380L' = https://...")
        print("\n   Presiona ENTER sin texto para terminar\n")
        
        image_urls = {}
        while True:
            try:
                user_input = input("Producto (ID o Nombre) = URL: ").strip()
                if not user_input:
                    break
                
                if "=" not in user_input:
                    print("   ⚠️  Formato incorrecto. Usa: ID o Nombre = URL")
                    continue
                
                key, url = user_input.split("=", 1)
                key = key.strip()
                url = url.strip()
                
                if not url.startswith("http"):
                    print("   ⚠️  La URL debe comenzar con http:// o https://")
                    continue
                
                image_urls[key] = url
                print(f"   ✅ Agregado: {key}")
                
            except KeyboardInterrupt:
                print("\n\n❌ Cancelado por el usuario")
                return
            except Exception as e:
                print(f"   ⚠️  Error: {e}")
    
    # Actualizar productos
    updated_count = 0
    for product in products:
        product_id = str(product["id"])
        product_name = product["name"]
        
        # Buscar por ID primero
        if product_id in image_urls:
            product["image"] = image_urls[product_id]
            updated_count += 1
            print(f"✅ Actualizado ID {product_id}: {product_name[:50]}")
            continue
        
        # Buscar por nombre (coincidencia parcial)
        for key, url in image_urls.items():
            if key.lower() in product_name.lower() or product_name.lower() in key.lower():
                product["image"] = url
                updated_count += 1
                print(f"✅ Actualizado: {product_name[:50]}")
                break
    
    # Guardar cambios
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"\n✨ Actualización completada!")
    print(f"   Productos actualizados: {updated_count}/{len(products)}")
    print(f"   Archivo guardado en: {json_path}")


def update_from_dict(image_dict: dict):
    """
    Actualiza imágenes desde un diccionario
    
    Args:
        image_dict: Diccionario con formato {id: url} o {name: url}
    """
    update_jumbo_images(image_dict)


if __name__ == "__main__":
    # Si se pasan argumentos como JSON, usarlos
    if len(sys.argv) > 1:
        try:
            import json
            image_data = json.loads(sys.argv[1])
            update_jumbo_images(image_data)
        except json.JSONDecodeError:
            print("❌ Error: El argumento debe ser un JSON válido")
            print("   Ejemplo: python update_jumbo_images.py '{\"1\": \"https://...\"}'")
    else:
        # Modo interactivo
        update_jumbo_images()
