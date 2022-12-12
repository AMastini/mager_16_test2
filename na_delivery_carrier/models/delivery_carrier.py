# -- coding: utf-8 --
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, models, fields, api
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError, ValidationError


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    weight_coefficent = fields.Float(string="Weight Coefficient", store=True)
    increment = fields.Float(string="Increment", store=True)
    insurance_rate = fields.Integer(string="Insurance rate", store=True)
    active_insurance = fields.Boolean(string="Is the insurance Active", store=True)

    def check_insurance_active(self, active):
        return active;

    def _get_price_available(self, order):
        self.ensure_one()
        self = self.sudo()
        order = order.sudo()
        total = weight = volume = quantity = 0
        total_delivery = 0.0
        for line in order.order_line:
            if line.state == 'cancel':
                continue
            if line.is_delivery:
                total_delivery += line.price_total
            if not line.product_id or line.is_delivery:
                continue
            if line.product_id.type == "service":
                continue
            qty = line.product_uom._compute_quantity(line.product_uom_qty, line.product_id.uom_id)
            for rule_line in self.price_rule_ids:
                if rule_line.custom_rule == 'normal_rule':
                    weight += (line.product_id.weight or 0.0) * qty
                else:
                    weight += ((line.product_id.weight + line.product_id.packing_weight) or 0.0)
            volume += (line.product_id.volume or 0.0) * qty
            quantity += qty
        total = (order.amount_total or 0.0) - total_delivery

        total = self._compute_currency(order, total, 'pricelist_to_company')

        return self._get_custom_price_from_picking(total, weight, volume, quantity)

    def _get_custom_price_from_picking(self, total, weight, volume, quantity):
        price = 0.0
        criteria_found = False
        price_dict = self._get_price_dict(total, weight, volume, quantity)
        if self.free_over and total >= self.amount:
            return 0
        for line in self.price_rule_ids:
            if line.custom_rule == 'normal_rule':
                test = safe_eval(line.variable + line.operator + str(line.max_value), price_dict)
                if test:
                    price = line.list_base_price + line.list_price * price_dict[line.variable_factor]
                    criteria_found = True
                    break
            else:
                # ((Coefficiente peso * (Peso netto + Peso imballo) + Incremento) * Quantità ordinata) *(1 + Aliquota assicurazione)
                price = ((line.weight_coefficent * price_dict['weight'] + line.increment) * price_dict['quantity']) * (
                        1 + line.insurance_rate)
                criteria_found = True
                break
        if not criteria_found:
            raise UserError(_("No price rule matching this order; delivery cost cannot be computed."))

        return price
