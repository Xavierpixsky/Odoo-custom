
from odoo import fields, models

class RegistroDeSessionOff(models.Model):
    _name = 'registro.de.session.off'
    _description = 'Registro de cierre de sesiones'

    name = fields.Char(string='Nombre', required=True)
    date = fields.Date(string='Fecha')
    description = fields.Text(string='Descripción')
    usuarios_afectados = fields.Many2many('res.users', string='Usuarios Afectados')