# -- coding: utf-8 --
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class WebsiteLocation(models.Model):
    _name = 'website.location'

    website_id = fields.Many2one('website', 'WebSite')
    is_in = fields.Boolean('In', default=True)
    country_ids = fields.Many2many("res.country", string='Countries')

    @api.model
    def qweb_track(self):
        # TODO: Define way to set all pages to track = True
        qweb_views = self.env['website.page'].search([])
        for qweb_view in qweb_views:
            qweb_view.track = True

        # Fixme [MPAGANI]: Faster code
        # qweb_views = self.env['website.page'].search([('track', '!=', True)])
        # if qweb_views:
        #     qweb_views.write({'track': True})

    def is_it_allowed(self, website, country):
        rule = self.env['website.location'].search([('website_id', '=', website.id)], order='create_date', limit=1)
        if not rule:
            return True
        if country and ((country in rule.country_ids) is rule.is_in):
            return True
        else:
            return False
        # Fixme [MPAGANI]: less code lines
        # if not rule or (country and ((country in rule.country_ids) is rule.is_in)):
        #     return True
        # return False
