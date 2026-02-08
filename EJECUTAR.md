# 🚀 CÓMO EJECUTAR LA APLICACIÓN

## Un solo comando (recomendado)

**Windows:** Haz doble clic en **`EJECUTAR.bat`**  
O en CMD/PowerShell, desde la carpeta del proyecto:
```bash
.\EJECUTAR.bat
```
Eso inicializa los datos si hace falta y arranca el servidor. Abre **http://127.0.0.1:8000** en el navegador.

---

## Opción 2: Ejecución manual (paso a paso)

### Paso 1: Abrir Terminal
Abre PowerShell o CMD en la **raíz del proyecto** (donde están las carpetas `backend/`, `frontend/` y `data/`):
```powershell
cd c:\Users\victo\Downloads\DELIVERY-main
```

### Paso 2: Instalar Dependencias (Solo la primera vez)
Desde la raíz del proyecto:
```bash
pip install -r backend/requirements.txt
```

### Paso 3: Inicializar Datos
```bash
python backend/init_data.py
```

### Paso 4: Iniciar el Servidor
Desde la raíz del proyecto:
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```
**Nota:** En Windows, `--reload` puede dar error. Usa el comando anterior (sin `--reload`). Si cambias código, detén el servidor (CTRL+C) y vuelve a ejecutarlo.

### Paso 5: Abrir en el Navegador
Abre tu navegador y ve a:
- **http://127.0.0.1:8000** - Página principal
- **http://127.0.0.1:8000/delivery** - Módulo de delivery
- **http://127.0.0.1:8000/api/docs** - Documentación API

---

## Opción 3: Comandos rápidos

### Todo en uno (si ya tienes dependencias instaladas):
```bash
python backend/init_data.py && python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

---

## ⚠️ Solución de Problemas

### Si aparece "uvicorn no se reconoce":
```bash
pip install uvicorn
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

### Si al iniciar sale error con "SpawnProcess" o "config.load()" (Windows):
En Windows, **no uses** `--reload`. Ejecuta:
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

### Si hay errores de importación:
Asegúrate de estar en la **raíz del proyecto** (donde están `backend/`, `frontend/`, `data/`):
```bash
cd c:\Users\victo\Downloads\DELIVERY-main
```

### Si el puerto 8000 está ocupado:
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8001
```

---

## 📋 Estado Actual

✅ **Servidor corriendo**: http://127.0.0.1:8000
✅ **Datos inicializados**: 15 negocios, productos, repartidores (ejecuta `python backend/init_data.py` si no)

---

## 🛑 Detener el Servidor

Presiona `CTRL + C` en la terminal donde está corriendo el servidor.
