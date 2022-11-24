# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software PVT. LTD.
# See LICENSE file for full copyright & licensing details.

# Author: Aktiv Software PVT. LTD.
# mail:   odoo@aktivsoftware.com
# Copyright (C) 2015-Present Aktiv Software PVT. LTD.
# Contributions:
#           Aktiv Software:
#              - Kinjal Lalani
#              - Surabh Yadav
#              - Tanvi Gajera
{
    'name': 'User Location',
    'summary': "Here user's location is fetched",
    'description': """ This module will help admin to see the login details
            of user like date, country, state and city""",
    'version': '14.0.1.0.0',
    'license': "AGPL-3",
    'author': "Aktiv Software",
    'category': 'Extra Tools',
    'depends': ['base'],
    'website': 'www.aktivsoftware.com',
    'data': [
        'views/res_user.xml',
    ],

    'images': ['static/description/banner.jpg'],
    'installable': True,
    'auto_install': False,
}
