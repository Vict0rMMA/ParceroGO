# Resumen de optimización del código

Refactor conservador aplicado para reducir líneas y redundancia sin alterar comportamiento, diseño ni funcionalidad. El proyecto se mantiene igual para el usuario y para revisión académica.

---

## Backend

### `backend/app/routes/delivery.py`

- **Helpers reutilizables**
  - `_get_all_products()`: centraliza la carga de `products.json` + `jumbo_products.json`. Antes esta concatenación se repetía en `create_order`, `add_to_cart`, `remove_from_cart` y `get_all_products`.
  - `_find(seq, key, value)`: devuelve el primer elemento de una lista donde `elem[key] == value`, o `None`. Sustituye repeticiones de `next((x for x in seq if x.get(key) == value), None)` en búsqueda de negocio, pedido, producto y repartidor.
- **Normalización de teléfono**: la condición de retorno en `_normalize_phone_for_match` se simplificó a un único `return` con expresión condicional.
- **Docstrings**: se acortaron donde no aportaban información nueva; se mantiene la documentación útil para cada endpoint.
- **Efecto**: menos líneas, misma lógica y mismas respuestas de la API.

---

## Frontend

### `frontend/static/delivery.js`

- **Formato de precios**
  - `formatPrice(val)`: unifica el uso de `formatCOP` (si existe) o `toLocaleString('es-CO')`. Se reemplazaron varias repeticiones en productos, lista de seleccionados y totales.
- **Escape de HTML/atributos**
  - `escapeHtml(str)`: reemplaza `<` y `>` para contenido seguro.
  - `escapeAttr(str)`: usa `escapeHtml` y además escapa `"` para atributos (p. ej. `alt=""`). Se usa en nombre y categoría de negocio y en nombre de producto en la tarjeta.
- **Agrupación por categoría**
  - `buildByCategory(arr)`: construye el objeto `{ categoría: [negocios] }` una sola vez. `groupByCategory` y `flatOrderByCategory` pasan a usar este resultado en lugar de duplicar el mismo bucle.
- **Efecto**: mismo aspecto y comportamiento; código más corto y fácil de mantener.

---

## Qué no se modificó

- **Otras rutas** (`payments`, `couriers`, `notifications`, `orders`): se dejaron igual para no introducir acoplamiento entre módulos ni cambios de comportamiento.
- **main.py**: las rutas de páginas HTML se mantienen explícitas para que la estructura siga siendo clara.
- **CSS, HTML, textos, rutas y flujos**: sin cambios.
- **Sin nuevas librerías ni cambios de framework.**

---

## Criterios aplicados

- Eliminar código duplicado.
- Unificar funciones repetidas en helpers con nombres claros.
- Simplificar condiciones y expresiones sin cambiar la lógica.
- Mantener nombres y estructura que ya se usan en el resto del proyecto.
- Estilo conservador y legible para revisión académica.
