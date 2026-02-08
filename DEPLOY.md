# Desplegar ParceroGo

Este proyecto tiene **backend en Python (FastAPI)**. Netlify solo sirve sitios estáticos, no ejecuta ese servidor. Por eso hay dos despliegues:

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

## 2. Netlify (landing que enlaza a la app)

En Netlify se despliega solo una **página estática** que lleva a la app en Render.

1. Entra a **https://app.netlify.com** y conecta el mismo repo de GitHub.
2. Configuración del sitio:
   - **Build command:** `echo Build OK` (o deja el que use `netlify.toml`).
   - **Publish directory:** `netlify-public`
3. **Deploy site**.
4. Después del primer deploy en **Render**, copia la URL de tu servicio (ej: `https://parcerogo.onrender.com`).
5. En el repo, edita **`netlify-public/index.html`**: cambia la URL del botón “Ir a la app” por tu URL de Render (busca `parcerogo.onrender.com` y sustitúyela).
6. Vuelve a desplegar en Netlify (push al repo o “Trigger deploy” en Netlify).

Tu dominio de Netlify (ej: `algo.netlify.app`) mostrará esa landing; el botón llevará a la app en Render.

---

## Resumen

| Dónde    | Qué se despliega                          |
|----------|-------------------------------------------|
| **Render** | App completa (FastAPI + frontend + API). |
| **Netlify** | Solo la landing con el botón “Ir a la app”. |

Para que todo funcione: primero despliega en **Render** y luego (opcional) en **Netlify** usando la URL de Render en el botón.
