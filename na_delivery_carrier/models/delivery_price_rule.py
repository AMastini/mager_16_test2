# -- coding: utf-8 --
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, models, fields, api


class DeliveryPriceRule(models.Model):
    _inherit = 'delivery.price.rule'

    custom_rule = fields.Selection(
        [('normal_rule', 'Standard Rule'), ('custom_rule_1', '3 Variables Rule')], default="normal_rule")

    weight_coefficent = fields.Float(string="Weight Coefficent",
                                     readonly=False, store=True, compute='_compute_weight_coefficent_value')
    increment = fields.Float(string="Increment", readonly=False,
                             store=True, compute='_compute_increment_value')
    insurance_rate = fields.Integer(string="Insurance rate",
                                    readonly=False, store=True, compute='_compute_insurance_rate_value')

    @api.depends('name')
    def _compute_weight_coefficent_value(self):
        for rule in self:
            rule.weight_coefficent = rule.carrier_id.weight_coefficent

    @api.depends('name')
    def _compute_increment_value(self):
        for rule in self:
            rule.increment = rule.carrier_id.increment

    @api.depends('name')
    def _compute_insurance_rate_value(self):
        for rule in self:
            rule.insurance_rate = rule.carrier_id.insurance_rate
