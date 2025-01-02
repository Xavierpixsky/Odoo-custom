# Usuario de Emergencia - PixSky Gestión de Seguridad

El módulo **PixSky Gestión de Seguridad** permite generar un usuario de emergencia temporal para acceder al sistema en situaciones críticas. Este usuario se crea al visitar una URL protegida y puede ser eliminado después de su uso.

---

## Datos del Usuario de Emergencia

- **Login:** `odooforemergency@odooservice.com`  
- **Contraseña Predeterminada:** `OdooRecovery@..v17`  
- **Grupos:**  
  - Administrador del sistema (`base.group_system`)  
  - Control de Sesiones (`pix_security.group_control_de_sesiones`)  
- **Duración:** Temporal (debe eliminarse manualmente tras su uso).  

**Nota:** Si deseas personalizar el login o contraseña, el módulo puede ser modificado, aunque los valores predeterminados son seguros y funcionales.

---

## Uso Rápido

1. **Generar el Usuario:**
   Accede a la URL protegida:

https://<tu_dominio_odoo>/emergency/odoo/help/secure/484290/99uu34u0uf9

2. **Inicia Sesión:**  
Usa el login y contraseña proporcionados para acceder.

3. **Ejecuta las Acciones Necesarias:**  
- Restaurar accesos: **PixSky Seguridad > Restaurar Sesiones**.  
- Cerrar sesiones: **PixSky Seguridad > Cerrar Sesiones**.

4. **Elimina el Usuario:**  
Al finalizar, elimina el usuario desde **Configuración > Usuarios y Compañías > Usuarios**.

---

## Recomendaciones

- **Protección de la URL:** Solo personal autorizado debe acceder a la URL.
- **Uso Temporal:** Elimina el usuario después de su uso para asegurar el sistema.
- **Contraseña:** Cambia la contraseña si el usuario debe permanecer activo por más tiempo.

---

## Contacto

Para soporte o personalización:  
- **Xavier Orlov**    
- Sitio web: [www.pix-sky.com](https://www.pix-sky.com)



