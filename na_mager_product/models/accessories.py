# -- coding: utf-8 --
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class Accessories(models.Model):
    _name = "accessories"
    _description = "Model for handling accessories"

    name = fields.Char(string="Model")
    code = fields.Char(string="Code")
    description = fields.Char(string="Dimensions and Description")
    kit_type = fields.Selection(selection=[('mounting', "Mounting"), ('wiper', "Wiper")], string="Kit Type")
    display_category_id = fields.Many2one('display.category', string="Display Category", store=True)
