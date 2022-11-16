# -- coding: utf-8 --
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Nexapp ~ Mager Documents',
    'summary': 'This module is a custom version of Odoo Invoicing',
    'description': """Nexapp ~ Mager Invoice""",
    'version': '16.0.1.0',
    'depends': [
        'base',
        'contacts',
        'portal',
    ],
    'author': "Nexapp S.r.l.",
    'license': "AGPL-3",
    'maintainers': ["Nadia Dotti"],
    'website': 'https://www.webeasytech.com',
    'category': 'Accounting/Accounting',
    'data': [
        'security/ir.model.access.csv',
        'views/mager_invoice_views.xml',
        'views/mager_invoice_menu.xml',
        'views/mager_portal_templates.xml',
    ],
    'application': True
}
