# PixSky Gestión de Seguridad

**Versión:** 17.0.1.0  
**Autor:** Xavier Orlov  
**Licencia:** LGPL-3  
**Categoría:** Tools  
**Compatibilidad:** Odoo 17  

---

## Descripción

El módulo **PixSky Gestión de Seguridad** está diseñado para proporcionar un control avanzado sobre las sesiones activas de los usuarios en un sistema Odoo. Ofrece funcionalidades para cerrar sesiones activas, restaurar accesos modificados y registrar eventos relacionados, garantizando una administración eficiente y centralizada de las sesiones de usuario.

---

## Funcionalidad

### Uso funcional
1. **Cierre de sesiones activas:**
   - Permite desconectar usuarios internos específicos o todos los usuarios internos excepto el ejecutor.
   - Para desconectar usuarios especificos, seleccione cada uno de ellos en el may2many del form principal, para efectuar un cierre masivo, simplemente use el botón rojo de esa manera el unico que no se verá afectado, es su usuario.
   - Se modifica el campo `login` de los usuarios objetivo añadiendo un prefijo y un sufijo, invalidando sus sesiones activas.

2. **Restauración de logins:**
   - Restaura los valores originales del campo `login` para usuarios cuya sesión fue invalidada, asegurando el acceso nuevamente.

3. **Registro de acciones:**
   - Cada cierre o restauración de sesión genera un registro en el sistema con detalles como usuarios afectados, motivo y fecha de ejecución.

4. **Usuario de Emergencia:**
   - El módulo incluye una funcionalidad para generar un usuario temporal con privilegios administrativos en situaciones críticas.  
   - **Recomendación:** Revisa el archivo [user-emergency.md](./user-emergency.md) para obtener detalles completos sobre su configuración, uso y eliminación.

### Uso técnico
- **Edición del campo `login`:**
  - En lugar de eliminar sesiones directamente, este módulo utiliza un enfoque más seguro y rastreable: modifica el campo `login` de los usuarios, lo que invalida automáticamente las sesiones activas sin afectar otras configuraciones de usuario.

- **Modelos involucrados:**
  - `logout.session`: Gestiona las operaciones de cierre de sesiones.
  - `res.users`: Modelo de usuarios de Odoo, donde se realiza la modificación del campo `login`.

---

## Ventajas

1. **Seguridad y trazabilidad:**
   - Las modificaciones en el campo `login` aseguran que todas las acciones puedan ser revertidas fácilmente.
   - Cada operación es registrada, proporcionando auditoría completa.

2. **Escalabilidad:**
   - Funciona tanto en sistemas pequeños como en implementaciones de gran escala con múltiples usuarios.

3. **Personalización:**
   - La configuración del prefijo y sufijo garantiza flexibilidad en su implementación.

4. **Resiliencia:**
   - Evita riesgos asociados a eliminar sesiones directamente, lo que puede interferir con otros procesos de Odoo.

---

## Casos de uso

1. **Cierre preventivo durante mantenimiento:**
   - Desconectar a todos los usuarios internos antes de realizar tareas críticas en el sistema.

2. **Control de acceso en tiempo real:**
   - Invalida sesiones activas de usuarios comprometidos o con permisos revocados.

3. **Restauración rápida de accesos:**
   - Rehabilita accesos modificados tras finalizar tareas administrativas o solucionar problemas.

---

## Ideas para Extensiones

1. **Programar cierres automáticos:**
   - Integrar con `ir.cron` para programar cierres de sesiones recurrentes.

2. **Notificaciones a usuarios:**
   - Enviar correos electrónicos o notificaciones push a los usuarios cuando se invaliden o restauren sus sesiones.

3. **Historial avanzado:**
   - Crear un modelo separado para almacenar logs detallados de todas las acciones realizadas por el módulo.

4. **Restricciones basadas en roles:**
   - Permitir exclusiones de ciertos usuarios o roles durante el cierre masivo de sesiones.

---

## Instalación

1. Copia el módulo en el directorio de addons de tu instancia de Odoo.
2. Actualiza la lista de módulos:
   ```bash
   ./odoo-bin -u all


Nota importante
Para situaciones críticas, donde se requiere acceso administrativo inmediato, consulta el archivo user-emergency.md. Este archivo describe cómo generar un usuario de emergencia, su propósito, y las recomendaciones para su uso seguro