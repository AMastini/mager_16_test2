# -- coding: utf-8 --
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Nexapp ~ Mager Product',
    'summary': 'This module allows to manage Mager products',
    'description': """Nexapp ~ Mager product management""",
    'version': '16.0.1.0',
    'depends': [
        'base',
        'website',
        'website_sale',
        'product',
        'stock',
        'uom',
    ],
    'author': "Nexapp S.r.l.",
    'license': "AGPL-3",
    'maintainers': ["Alberto Mastini"],
    'website': 'https://www.webeasytech.com',
    'category': 'Inventory/Inventory',
    'data': [
        'security/project_security.xml',
        'security/ir.model.access.csv',
        'views/product_template_view.xml',
        'views/display_category_view.xml',
    ],
    'application': True
}
