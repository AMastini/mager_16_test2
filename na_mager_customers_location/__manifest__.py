# -- coding: utf-8 --
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Nexapp ~ Mager Customers Location',
    'summary': 'This module is used to trace the IP address of customers who visit the website',
    'description': """Nexapp ~ Mager Customers Location""",
    'version': '16.0.1.0',
    'depends': [
        'website',
    ],
    'author': "Nexapp S.r.l.",
    'license': "AGPL-3",
    'maintainers': ["Nadia Dotti"],
    'website': 'https://www.webeasytech.com',
    'category': 'Website',
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'views/website_location_views.xml',
    ],
    'application': False
}
