# Desplegar ParceroGo

Tienes dos opciones:

- **Vercel**: app completa estática (HTML + JS), misma UI y flujos que en local. Login, pedidos y pagos simulados en el navegador (localStorage). Sin backend.
- **Render**: app con backend Python (FastAPI); misma funcionalidad, los datos se guardan en el servidor.

---

## 1. Vercel (app estática — recomendado para MVP)

La app se despliega como sitio estático. Todo sigue siendo **simulado** (localStorage, sin API real).

### Build local (opcional)

```bash
npm run build
```

- **Comando de build:** `npm run build`
- **Carpeta de salida:** `out/`

### Pasos en Vercel

1. Entra a **https://vercel.com** y conecta tu repo de GitHub.
2. **Root Directory:** deja vacío (raíz del repo).
3. **Build Command:** `npm run build` (o el que tenga `vercel.json`).
4. **Output Directory:** `out` (debe coincidir con `vercel.json`).
5. **Framework Preset:** Other.
6. **Deploy.**

No hace falta configurar variables de entorno. La app usará `/data/*.json` (incluidos en el build) y `localStorage` para sesión y pedidos.

### Panel de Vercel

- **Build Command:** `npm run build`
- **Output Directory:** `out`
- No cambies **Root Directory** (debe ser la raíz del proyecto).

---

## 2. Render (app con backend Python)

La app entera (API + páginas) se despliega en **Render**.

1. Entra a **https://render.com** y crea cuenta (o inicia sesión).
2. **New** → **Web Service**.
3. Conecta tu repo de GitHub.
4. Render puede detectar el `render.yaml`; si no:
   - **Build command:** `pip install -r backend/requirements.txt`
   - **Start command:** `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Root directory:** (vacío = raíz del repo)
5. **Create Web Service**. Tu app quedará en una URL como `https://parcerogo.onrender.com`.

**Nota:** En el plan gratis el servicio se “duerme” tras inactividad; la primera visita puede tardar unos segundos.

---

## Resumen

| Dónde    | Qué se despliega |
|----------|-------------------|
| **Vercel** | App estática (HTML/JS), misma UI; datos simulados en localStorage. |
| **Render** | App completa con FastAPI (backend + frontend). |

Para ver la app igual que en local en un solo despliegue, usa **Vercel** con los pasos de la sección 1.
