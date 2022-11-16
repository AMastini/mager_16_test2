# -- coding: utf-8 --
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Nexapp ~ Mager Theme',
    'description': 'This is a theme made specifically for Mager, in particular it\'s going to be used for a new header and footer',
    'version': '15.0.1.0',
    'author': "Nexapp S.r.l.",
    'license': "AGPL-3",
    'maintainers': ["Alberto Mastini"],
    'website': 'https://www.webeasytech.com',
    'category': 'Theme/Creative',

    'depends': ['website', 'website_sale', 'website_profile', 'portal', 'na_mager_customers_location',
                'na_mager_product', 'na_mager_invoice', 'na_website_scroll_top_bytesfuel', ],
    'data': ['views/layout.xml',
             ],
    'assets': {
        'web.assets_frontend': [
            'theme_mager/static/scss/style.scss',
        ],
        'web.assets_backend': [
            'theme_mager/static/src/code.js',
        ],
    },
}
