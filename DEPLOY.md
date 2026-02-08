# Desplegar ParceroGo

Este proyecto tiene **backend en Python (FastAPI)**. Vercel sirve solo la landing estática; la app completa se despliega en Render.

---

## 1. App completa en Render (recomendado)

La app entera (API + páginas) se despliega en **Render**.

1. Entra a **https://render.com** y crea cuenta (o inicia sesión).
2. **New** → **Web Service**.
3. Conecta tu repo de GitHub (**VictorMMA/ParceroGO** o el que uses).
4. Render puede detectar el `render.yaml`:
   - Si no, configura a mano:
     - **Build command:** `pip install -r backend/requirements.txt`
     - **Start command:** `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
     - **Root directory:** (dejar vacío = raíz del repo)
5. **Create Web Service**. Espera a que termine el deploy.
6. Tu app quedará en una URL como:  
   `https://parcerogo.onrender.com`  
   (o el nombre que le hayas puesto al servicio).

**Nota:** En el plan gratis, el servicio se “duerme” tras inactividad; la primera visita puede tardar unos segundos en despertar.

---

## 2. Vercel (landing que enlaza a la app)

En Vercel se despliega solo la **página estática** que lleva a la app en Render.

1. Entra a **https://vercel.com** y conecta el mismo repo de GitHub.
2. Al crear el proyecto, en **Root Directory** elige **Edit** y pon: `landing`.
3. **Framework Preset:** Other (o deja que lo detecte como estático).
4. No hace falta Build Command; **Deploy**.
5. Después del primer deploy en **Render**, copia la URL de tu servicio (ej: `https://parcerogo.onrender.com`).
6. En el repo, edita **`landing/index.html`**: cambia la URL del botón “Ir a la app” por tu URL de Render (busca `parcerogo.onrender.com` y sustitúyela).
7. Vuelve a desplegar en Vercel (push al repo o redeploy desde el dashboard).

Tu dominio de Vercel (ej: `parcerogo.vercel.app`) mostrará la landing; el botón llevará a la app en Render.

---

## Resumen

| Dónde    | Qué se despliega                          |
|----------|-------------------------------------------|
| **Render** | App completa (FastAPI + frontend + API). |
| **Vercel** | Solo la landing con el botón “Ir a la app”. |

Para que todo funcione: primero despliega en **Render** y luego (opcional) en **Vercel** usando la URL de Render en el botón.
