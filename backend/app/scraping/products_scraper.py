"""
Módulo de scraping para obtener productos de los negocios

Genera datos de productos simulados organizados por categoría de negocio.
Los productos incluyen información de precio y descripción basada en
categorías comerciales reales.
"""

import json
import random
from typing import List, Dict

# Catálogo de productos por categoría de negocio
PRODUCTS_BY_CATEGORY = {
    "Restaurante": [
        {"name": "Bandeja Paisa", "price": 25000, "description": "Plato típico antioqueño", "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=400&fit=crop"},
        {"name": "Sancocho", "price": 18000, "description": "Sopa tradicional", "image": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400&h=400&fit=crop"},
        {"name": "Hamburguesa", "price": 15000, "description": "Hamburguesa artesanal", "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400&h=400&fit=crop"},
        {"name": "Pizza Personal", "price": 12000, "description": "Pizza mediana", "image": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400&h=400&fit=crop"},
        {"name": "Salchipapa", "price": 8000, "description": "Salchipapa especial", "image": "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=400&h=400&fit=crop"},
    ],
    "Comidas Rápidas": [
        {"name": "Hamburguesa Clásica", "price": 12000, "description": "Hamburguesa con papas", "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400&h=400&fit=crop"},
        {"name": "Perro Caliente", "price": 8000, "description": "Perro caliente especial", "image": "https://images.unsplash.com/photo-1619740452663-6b4b8723c6b3?w=400&h=400&fit=crop"},
        {"name": "Papa Rellena", "price": 10000, "description": "Papa rellena de carne", "image": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=400&h=400&fit=crop"},
        {"name": "Arepa Rellena", "price": 6000, "description": "Arepa con queso y huevo", "image": "https://images.unsplash.com/photo-1603123853887-a92fafb7809f?w=400&h=400&fit=crop"},
        {"name": "Empanadas", "price": 3000, "description": "Empanadas de carne", "image": "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=400&h=400&fit=crop"},
        {"name": "Chorizo con Arepa", "price": 7000, "description": "Chorizo parrillero", "image": "https://images.unsplash.com/photo-1603123853887-a92fafb7809f?w=400&h=400&fit=crop"},
        {"name": "Alitas de Pollo", "price": 15000, "description": "Alitas BBQ o Buffalo", "image": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=400&h=400&fit=crop"},
        {"name": "Nachos", "price": 11000, "description": "Nachos con queso", "image": "https://images.unsplash.com/photo-1513456852971-30c0b8199d4d?w=400&h=400&fit=crop"},
    ],
    "Tienda de Abarrotes": [
        {"name": "Arroz 1kg", "price": 3500, "description": "Arroz premium", "image": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=400&fit=crop"},
        {"name": "Aceite 1L", "price": 8500, "description": "Aceite de cocina", "image": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400&h=400&fit=crop"},
        {"name": "Azúcar 1kg", "price": 2800, "description": "Azúcar blanca", "image": "https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=400&h=400&fit=crop"},
        {"name": "Sal 500g", "price": 1500, "description": "Sal refinada", "image": "https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=400&h=400&fit=crop"},
        {"name": "Frijoles 500g", "price": 3200, "description": "Frijoles rojos", "image": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=400&fit=crop"},
    ],
    "Farmacia": [
        {"name": "Acetaminofén", "price": 5000, "description": "Analgésico 500mg", "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&h=400&fit=crop"},
        {"name": "Ibuprofeno", "price": 6000, "description": "Antiinflamatorio", "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&h=400&fit=crop"},
        {"name": "Alcohol", "price": 3500, "description": "Alcohol antiséptico 500ml", "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&h=400&fit=crop"},
        {"name": "Vendas", "price": 4500, "description": "Vendas elásticas", "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&h=400&fit=crop"},
        {"name": "Jabón Antibacterial", "price": 2500, "description": "Jabón líquido", "image": "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=400&h=400&fit=crop"},
    ],
    "Panadería": [
        {"name": "Pan de Bono", "price": 500, "description": "Pan de bono tradicional", "image": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&h=400&fit=crop"},
        {"name": "Almojábana", "price": 600, "description": "Almojábana fresca", "image": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&h=400&fit=crop"},
        {"name": "Pandebono", "price": 500, "description": "Pandebono artesanal", "image": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&h=400&fit=crop"},
        {"name": "Rosca", "price": 800, "description": "Rosca dulce", "image": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&h=400&fit=crop"},
        {"name": "Pan Integral", "price": 3000, "description": "Pan integral 500g", "image": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&h=400&fit=crop"},
    ],
    "Supermercado": [
        {"name": "Leche 1L", "price": 4500, "description": "Leche entera", "image": "https://images.unsplash.com/photo-1563636619-914057cff423?w=400&h=400&fit=crop"},
        {"name": "Huevos x12", "price": 8000, "description": "Huevos AA", "image": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=400&h=400&fit=crop"},
        {"name": "Pan Tajado", "price": 2500, "description": "Pan de molde", "image": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&h=400&fit=crop"},
        {"name": "Queso 250g", "price": 5500, "description": "Queso campesino", "image": "https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?w=400&h=400&fit=crop"},
        {"name": "Yogurt", "price": 2800, "description": "Yogurt natural", "image": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400&h=400&fit=crop"},
    ],
    "Cafetería": [
        {"name": "Café Tinto", "price": 2000, "description": "Café colombiano", "image": "https://images.unsplash.com/photo-1517487881594-2787fef5ebf7?w=400&h=400&fit=crop"},
        {"name": "Cappuccino", "price": 4500, "description": "Cappuccino italiano", "image": "https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=400&h=400&fit=crop"},
        {"name": "Latte", "price": 5000, "description": "Latte artesanal", "image": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400&h=400&fit=crop"},
        {"name": "Té Verde", "price": 3500, "description": "Té verde natural", "image": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400&h=400&fit=crop"},
        {"name": "Pastel", "price": 4000, "description": "Pastel casero", "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400&h=400&fit=crop"},
    ],
    "Veterinaria": [
        {"name": "Alimento para Perro 15kg", "price": 85000, "description": "Alimento premium", "image": "https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=400&h=400&fit=crop"},
        {"name": "Alimento para Gato 7kg", "price": 45000, "description": "Alimento balanceado", "image": "https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=400&h=400&fit=crop"},
        {"name": "Juguete para Mascota", "price": 12000, "description": "Juguete interactivo", "image": "https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=400&h=400&fit=crop"},
        {"name": "Correa", "price": 15000, "description": "Correa ajustable", "image": "https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=400&h=400&fit=crop"},
        {"name": "Shampoo para Mascotas", "price": 18000, "description": "Shampoo hipoalergénico", "image": "https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=400&h=400&fit=crop"},
    ],
    "Tienda de Mascotas": [
        {"name": "Cama para Perro", "price": 45000, "description": "Cama cómoda", "image": "https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=400&h=400&fit=crop"},
        {"name": "Plato Comedero", "price": 8000, "description": "Plato acero inoxidable", "image": "https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=400&h=400&fit=crop"},
        {"name": "Collar", "price": 12000, "description": "Collar ajustable", "image": "https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=400&h=400&fit=crop"},
        {"name": "Snacks para Perro", "price": 15000, "description": "Snacks naturales", "image": "https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=400&h=400&fit=crop"},
        {"name": "Arenero para Gato", "price": 35000, "description": "Arenero con pala", "image": "https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=400&h=400&fit=crop"},
    ],
    "Pizzería": [
        {"name": "Pizza Margherita", "price": 18000, "description": "Pizza clásica con tomate, mozzarella y albahaca", "image": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400&h=400&fit=crop"},
        {"name": "Pizza Pepperoni", "price": 22000, "description": "Pizza con pepperoni y queso", "image": "https://images.unsplash.com/photo-1628840042765-356cda07504e?w=400&h=400&fit=crop"},
        {"name": "Pizza Hawaiana", "price": 20000, "description": "Pizza con jamón y piña", "image": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400&h=400&fit=crop"},
        {"name": "Pizza Cuatro Quesos", "price": 25000, "description": "Pizza con cuatro tipos de queso", "image": "https://images.unsplash.com/photo-1571997478779-2adcbbe9ab2f?w=400&h=400&fit=crop"},
        {"name": "Pizza Vegetariana", "price": 19000, "description": "Pizza con verduras frescas", "image": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400&h=400&fit=crop"},
        {"name": "Pizza Napolitana", "price": 21000, "description": "Pizza estilo italiano tradicional", "image": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400&h=400&fit=crop"},
        {"name": "Pizza de Pollo BBQ", "price": 23000, "description": "Pizza con pollo y salsa BBQ", "image": "https://images.unsplash.com/photo-1628840042765-356cda07504e?w=400&h=400&fit=crop"},
        {"name": "Pizza Familiar", "price": 35000, "description": "Pizza grande para compartir", "image": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400&h=400&fit=crop"},
    ],
}


def scrape_products(businesses: List[Dict]) -> List[Dict]:
    """
    Genera productos para cada negocio basado en su categoría
    
    Args:
        businesses: Lista de negocios para los cuales generar productos
        
    Returns:
        Lista de productos asociados a los negocios
    """
    products = []
    product_id = 1
    
    for business in businesses:
        category = business["category"]
        category_products = PRODUCTS_BY_CATEGORY.get(category, PRODUCTS_BY_CATEGORY["Tienda de Abarrotes"])
        
        # Seleccionar entre 3 y 5 productos aleatorios por negocio
        num_products = random.randint(3, 5)
        selected_products = random.sample(category_products, min(num_products, len(category_products)))
        
        for prod_template in selected_products:
            product = {
                "id": product_id,
                "business_id": business["id"],
                "name": prod_template["name"],
                "price": prod_template["price"],
                "description": prod_template["description"],
                "category": category,
                "available": random.choice([True, True, True, False]),  # 75% disponible
                "image": prod_template.get("image", f"https://via.placeholder.com/300x300?text={prod_template['name'].replace(' ', '+')}")
            }
            products.append(product)
            product_id += 1
    
    return products


def save_products(businesses: List[Dict]):
    """
    Genera y guarda los productos en un archivo JSON
    
    Args:
        businesses: Lista de negocios para los cuales generar productos
        
    Returns:
        Lista de productos generados
    """
    products = scrape_products(businesses)
    with open("data/products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    print(f"Guardados {len(products)} productos en data/products.json")
    return products


if __name__ == "__main__":
    # Cargar negocios primero
    import json
    with open("data/businesses.json", "r", encoding="utf-8") as f:
        businesses = json.load(f)
    save_products(businesses)
