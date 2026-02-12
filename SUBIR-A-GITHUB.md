# Subir ParceroGO a GitHub – paso a paso

## ✅ Hecho
- Repositorio Git en esta carpeta.
- Remoto `origin`: https://github.com/Vict0rMMA/ParceroGO.git
- Merge con GitHub resuelto (se conservó tu versión local).
- **Push realizado**: el proyecto está en https://github.com/Vict0rMMA/ParceroGO

---

## Comando para subir (ejecuta en terminal)

Abre **PowerShell** o **Terminal** en Cursor y ejecuta:

```powershell
cd "c:\Users\victo\Downloads\ParceroGO-main"
git push -u origin main
```

---

## Si te pide iniciar sesión

1. **Si se abre el navegador**: inicia sesión en GitHub y autoriza. Luego vuelve a la terminal y el `git push` seguirá solo.

2. **Si pide usuario y contraseña**:
   - **Usuario**: tu usuario de GitHub (ej: `Vict0rMMA`).
   - **Contraseña**: no uses la contraseña de GitHub. Usa un **Personal Access Token**:
     - Entra a GitHub → Settings → Developer settings → Personal access tokens.
     - "Generate new token (classic)".
     - Marca al menos `repo`.
     - Copia el token y pégalo donde te pide la contraseña.

3. **Si dice "support for password authentication was removed"**: entonces debes usar el token como en el punto 2.

---

## Resumen de comandos (copiar y pegar)

```powershell
cd "c:\Users\victo\Downloads\ParceroGO-main"
git push -u origin main
```

Después de esto, tu código estará en: https://github.com/Vict0rMMA/ParceroGO
