# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.http import request


class ResPartner(models.Model):
    _inherit = 'res.partner'

    default_incoterm_id = fields.Many2one(
        "account.incoterms", related="country_id.default_incoterm_id")
    privacy_accepted = fields.Char(string="Has accepted privacy", readonly=True)

    def retrieve_country_state_zip(self, country_id):
        fiscal_position_obj = self.env['account.fiscal.position']
        fp = fiscal_position_obj._get_fpos_by_country(country_id)
        return fp

    @api.model
    def create(self, vals):
        country_id = self.env['website.visitor'].get_country_id()
        vals.update(
            {
            'property_account_position_id': self.retrieve_country_state_zip(country_id).id,
            'privacy_accepted': request.params['privacy_acceptance'],
            })

        res = super(ResPartner, self).create(vals)
        return res
