from odoo import models, fields, api
from odoo.exceptions import UserError

class LogoutSession(models.Model):
    _name = 'logout.session'
    _description = 'Gestión de Cierre de Sesiones de Usuarios'

    name = fields.Char(string='Descripción', required=True, default="Cierre de Sesiones")
    targeted_users = fields.Many2many('res.users', string='Usuarios a Desconectar', help="Selecciona usuarios específicos para desconectar. Si está vacío, se desconectarán todos los usuarios internos excepto el ejecutante.")
    motivos = fields.Text(string='Motivo de la Acción')

    PREFIX = "DISABLED_USER_"
    SUFFIX = "_SESSION_BLOCKED"

    def call_logout_sessions(self):
        """ Invalida las sesiones activas de usuarios específicos o de todos los usuarios internos excepto el actual y registra la acción """
        try:
            # Obtener el usuario actual
            current_user = self.env.user

            # Determinar los usuarios objetivo
            if self.targeted_users:
                # Si se especifican usuarios en el campo Many2many
                users_to_logout = self.targeted_users.filtered(lambda user: user.id != current_user.id)
                if not users_to_logout:
                    raise UserError("No puedes desconectarte a ti mismo ni desconectar usuarios inválidos.")
            else:
                # Si no se especifican usuarios, aplica a todos los usuarios internos excepto el actual
                users_to_logout = self.env['res.users'].search([
                    ('id', '!=', current_user.id),
                    ('login', '!=', False),  # Usuarios con login válido
                    ('share', '=', False)   # Excluir usuarios externos
                ])

            if not users_to_logout:
                raise UserError("No se encontraron usuarios internos activos para desconectar.")

            # Invalida las sesiones activas añadiendo prefijo y sufijo al campo `login`
            for user in users_to_logout:
                user.sudo().write({'login': f"{self.PREFIX}{user.login}{self.SUFFIX}"})

            # Crear un registro en el modelo `registro.de.session.off`
            self.env['registro.de.session.off'].create({
                'name': self.name,
                'date': fields.Date.context_today(self),
                'description': self.motivos or "Cierre de sesiones ejecutado",
                'usuarios_afectados': [(6, 0, users_to_logout.ids)]
            })

            # Limpiar los campos `targeted_users` y `motivos`
            self.targeted_users = [(5, 0, 0)]
            self.motivos = False

        except Exception as e:
            raise UserError(f"Error inesperado al cerrar sesiones: {str(e)}")

    def restore_logins(self):
        """ Restaura los logins originales eliminando el prefijo y sufijo """
        try:
            # Buscar usuarios con logins modificados
            invalid_users = self.env['res.users'].search([('login', 'like', f"{self.PREFIX}%{self.SUFFIX}")])

            if not invalid_users:
                raise UserError("No se encontraron usuarios con logins inválidos para restaurar.")

            # Restaurar logins originales eliminando prefijo y sufijo
            for user in invalid_users:
                original_login = user.login.replace(self.PREFIX, '').replace(self.SUFFIX, '')
                user.sudo().write({'login': original_login})

            return {
                'status': 'success',
                'message': f"Logins de {len(invalid_users)} usuarios restaurados con éxito.",
            }

        except Exception as e:
            raise UserError(f"Error inesperado al restaurar logins: {str(e)}")