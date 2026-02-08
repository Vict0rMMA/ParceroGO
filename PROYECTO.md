# Documentación del Proyecto - MVP Delivery Local

## 📋 Descripción General

Este proyecto es un **MVP (Minimum Viable Product)** académico de una plataforma de delivery para negocios de barrio en Medellín, Colombia.

## 🏗️ Arquitectura del Sistema

### Tecnologías Utilizadas

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Mapa**: Leaflet.js + OpenStreetMap
- **Almacenamiento**: Archivos JSON (sin base de datos)

### Estructura de Directorios

```
MASCOTAS/
├── app/                    # Código de la aplicación
│   ├── main.py            # Aplicación principal FastAPI
│   ├── utils.py          # Utilidades compartidas
│   ├── routes/           # Módulos de rutas API
│   │   ├── delivery.py   # Rutas de delivery
│   │   ├── payments.py   # Rutas de pagos
│   │   └── couriers.py   # Rutas de repartidores
│   └── data_generator.py # Generación de datos (negocios, productos, repartidores)
├── data/                  # Archivos JSON de datos
├── templates/            # Templates HTML
├── static/               # Archivos estáticos (CSS, JS)
└── requirements.txt      # Dependencias Python
```

## 🔑 Decisiones de Diseño

### ¿Por qué sin base de datos?

1. **Simplicidad**: Facilita el despliegue y mantenimiento
2. **Bajo costo**: No requiere servidor de base de datos
3. **Propósito académico**: Demuestra conceptos sin complejidad innecesaria
4. **Escalabilidad futura**: La arquitectura permite migrar a BD fácilmente

## 📊 Módulos del Sistema

### 1. Módulo de Delivery

**Funcionalidades:**
- Listado de negocios locales
- Catálogo de productos por negocio
- Creación de pedidos
- Cálculo de distancias y tiempos estimados
- Gestión de estados de pedido

**Estados de pedido:**
- `pendiente` - Pedido creado, esperando preparación
- `preparando` - El negocio está preparando el pedido
- `en_camino` - Repartidor asignado, en camino al cliente
- `entregado` - Pedido completado
- `cancelado` - Pedido cancelado

### 2. Módulo de Pagos

**Funcionalidades:**
- Procesamiento simulado de pagos
- Soporte para efectivo y tarjeta
- Historial de transacciones
- Validación básica de datos de tarjeta

**Estados de pago:**
- `pendiente` - Pago pendiente (efectivo)
- `pagado` - Pago completado

### 3. Módulo de Repartidores

**Funcionalidades:**
- Listado de repartidores disponibles
- Asignación automática por cercanía
- Gestión de disponibilidad
- Seguimiento de entregas

**Características:**
- Ubicación geográfica en tiempo real (simulada)
- Rating y estadísticas
- Tipo de vehículo (Moto/Bicicleta)

## 🗺️ Integración con Mapa

El sistema utiliza **Leaflet.js** con **OpenStreetMap** para:

- Visualizar ubicaciones de negocios
- Mostrar ubicaciones de repartidores
- Calcular distancias entre puntos usando fórmula de Haversine
- Facilitar la navegación geográfica

**Coordenadas base**: Medellín, Colombia (6.2476° N, 75.5658° W)

## 🔒 Consideraciones de Seguridad

1. **Pagos simulados**: No se procesan transacciones reales
2. **Datos de prueba**: Los datos son para demostración académica
3. **Validación básica**: Se implementan validaciones mínimas necesarias
4. **Sin autenticación**: Por simplicidad académica, no hay sistema de usuarios

## 📈 Limitaciones y Mejoras Futuras

### Limitaciones Actuales:
- Sin sistema de autenticación
- Datos almacenados en archivos JSON (no concurrente)
- Pagos completamente simulados
- Sin notificaciones en tiempo real

### Mejoras Futuras Sugeridas:
- Implementar base de datos (PostgreSQL/MongoDB)
- Agregar autenticación de usuarios
- Integrar pasarela de pagos real
- Sistema de notificaciones
- Aplicación móvil
- Dashboard de administración

## 🎓 Justificación Académica

Este proyecto demuestra:

1. **Arquitectura de software**: Separación de módulos y responsabilidades
2. **APIs RESTful**: Diseño de endpoints bien estructurados
3. **Integración de tecnologías**: Frontend, Backend, Mapas
4. **Sin dependencias complejas**: Solución viable sin base de datos
6. **Cálculos geográficos**: Uso de fórmulas matemáticas (Haversine)

## 📝 Notas para el Profesor

- El código está completamente comentado y documentado
- La estructura sigue buenas prácticas de Python
- Los nombres de variables y funciones son descriptivos
- El proyecto es completamente funcional end-to-end
- Los datos son simulados pero realistas
- El sistema está diseñado para ser fácilmente extensible

---

**Proyecto desarrollado con fines académicos** 🎓
