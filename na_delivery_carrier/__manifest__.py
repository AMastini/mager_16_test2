# -- coding: utf-8 --
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Nexapp Delivery Carrier',
    'summary': 'This module allows to manage Custom Delivery Shipping Costs Rules',
    'description': """Nexapp module to create new delivery rules""",
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
    'category': 'Inventory/Delivery',
    'data': [
        'security/ir.model.access.csv',
        'views/delivery_views.xml',
        'views/delivery_layout.xml',
    ],
}
