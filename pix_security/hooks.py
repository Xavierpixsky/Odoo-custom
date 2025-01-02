from odoo import api, SUPERUSER_ID

def create_default_logout_session(env):
    """
    Crea el registro inicial para logout.session al instalar el módulo.
    """
    if not env['logout.session'].sudo().search([('id', '=', 1)]):
        env['logout.session'].sudo().create({
            'id': 1,
            'name': 'Gestión Inicial de Cierre de Sesiones',
        })
