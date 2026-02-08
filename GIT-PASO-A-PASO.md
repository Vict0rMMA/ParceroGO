# Guía paso a paso: subir ParceroGo a GitHub

## Parte 1: Crear el repositorio en GitHub

1. Entra a **https://github.com** e inicia sesión.
2. Clic en el **+** (arriba derecha) → **New repository**.
3. **Repository name:** `ParceroGO` (o el nombre que quieras).
4. Elige **Public**.
5. **No** marques "Add a README", "Add .gitignore" ni "Choose a license" (el proyecto ya tiene archivos).
6. Clic en **Create repository**.
7. Anota la URL que te muestra GitHub, por ejemplo:
   - `https://github.com/TU_USUARIO/ParceroGO.git`  
   (reemplaza **TU_USUARIO** por tu usuario real, por ejemplo `Vict0rMMA`).

---

## Parte 2: Configurar Git en tu PC (solo la primera vez)

1. Abre **PowerShell** o **Símbolo del sistema**.
2. Comprueba que Git esté instalado:
   ```powershell
   git --version
   ```
   Si no está instalado, descarga: https://git-scm.com/download/win

3. Configura tu nombre y email (solo una vez):
   ```powershell
   git config --global user.name "Tu Nombre"
   git config --global credential.helper manager
   ```
   (Opcional) Email:
   ```powershell
   git config --global user.email "tu@email.com"
   ```

---

## Parte 3: Inicializar el proyecto e hizo el primer commit

1. Abre PowerShell y ve a la carpeta del proyecto:
   ```powershell
   cd c:\Users\victo\Downloads\DELIVERY-main
   ```

2. Inicializa Git (si aún no lo has hecho):
   ```powershell
   git init
   ```

3. Añade todos los archivos:
   ```powershell
   git add -A
   ```

4. Crea el primer commit:
   ```powershell
   git commit -m "Initial commit: ParceroGo MVP Delivery"
   ```

5. Pon la rama principal como `main`:
   ```powershell
   git branch -M main
   ```

---

## Parte 4: Conectar con GitHub y subir el código

1. Añade el remoto (cambia **TU_USUARIO** por tu usuario de GitHub):
   ```powershell
   git remote add origin https://github.com/TU_USUARIO/ParceroGO.git
   ```
   Si ya existe `origin` y quieres corregir la URL:
   ```powershell
   git remote set-url origin https://github.com/TU_USUARIO/ParceroGO.git
   ```

2. Sube el código:
   ```powershell
   git push -u origin main
   ```

3. Si te pide **usuario y contraseña**:
   - **Usuario:** tu usuario de GitHub (ej: `Vict0rMMA`).
   - **Contraseña:** no uses la contraseña de la cuenta. Usa un **Personal Access Token**:
     - GitHub → tu foto (arriba derecha) → **Settings**.
     - Abajo a la izquierda → **Developer settings** → **Personal access tokens** → **Tokens (classic)**.
     - **Generate new token (classic)**.
     - Pon un nombre (ej: "ParceroGO") y marca el permiso **repo**.
     - **Generate token** y **copia el token** (solo se muestra una vez).
     - Cuando Git pida "Password", pega ese token.

4. Comprueba en el navegador que tu repo tenga los archivos:  
   `https://github.com/TU_USUARIO/ParceroGO`

---

## Resumen rápido (si ya tienes repo en GitHub y Git configurado)

```powershell
cd c:\Users\victo\Downloads\DELIVERY-main
git init
git add -A
git commit -m "Initial commit: ParceroGo MVP Delivery"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/ParceroGO.git
git push -u origin main
```

(Si `origin` ya existe: `git remote set-url origin https://github.com/TU_USUARIO/ParceroGO.git` y luego `git push -u origin main`.)

---

## Errores frecuentes

| Error | Qué hacer |
|-------|-----------|
| **Repository not found** | Revisa que la URL tenga bien tu usuario (ej: `Vict0rMMA` con cero, no la letra O) y el nombre del repo. |
| **remote origin already exists** | Usa `git remote set-url origin https://github.com/TU_USUARIO/ParceroGO.git` para cambiar la URL. |
| **Support for password authentication was removed** | Debes usar un **Personal Access Token** como “contraseña”, no la contraseña de GitHub. |
| **failed to push** | Comprueba internet y que el token tenga permiso **repo**. |
