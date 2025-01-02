{
    'name': 'PixSky Gestión de Seguridad',
    'version': '17.0.1.0',
    'author': 'Xavier Orlov',
    'category': 'Tools',
    'summary': 'Cierra sesiones activas de usuarios internos.',
    'description': '''
        Este módulo permite cerrar todas las sesiones activas de usuarios internos excepto la del usuario que ejecuta la acción. 
        También registra los eventos de cierre de sesión.
    ''',
    'license': 'LGPL-3',
    'depends': ['base', 'web'],
    'data': [
        'security/control_de_sesiones.xml',
        'security/ir.model.access.csv',
        'views/logout_session.xml',
        'views/register_session.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pix_security/static/src/css/styles.css',
        ],
    },
    'installable': True,
    'application': True,
    'post_init_hook': 'create_default_logout_session',
    'images': ['pix_security/static/description/logo.png'],
}