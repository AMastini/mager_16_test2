# -- coding: utf-8 --
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # base data
    display_category_id = fields.Many2one('display.category', string="Display Category", store=True)
    rel_display_category_name = fields.Char(related='display_category_id.name',
                                            string="Display Category Name for Import")
    rel_display_category_parent = fields.Many2one(related="display_category_id.parent_id",
                                                  string="Display Category Parent for Import")
    series = fields.Char(string="Series Type", compute="_compute_series_type", store=True, default='hrp')
    support = fields.Boolean(string="Support version", compute="_compute_support", store=True)
    data_sheet = fields.Char(string="Data sheet")
    cad_3d = fields.Char(string="Cad 3D")
    pdf_drawing = fields.Char(string="Pdf Drawing")
    accessories = fields.Char(string="Accessories")
    accessories_cad_3d = fields.Char(string="Accessories Cad 3D")
    image = fields.Char(string="Image URL")

    # airc data
    air_consumption_min = fields.Float(string="Air consumption min.")
    air_consumption_max = fields.Float(string="Air consumption max.")
    max_stiffness_air_consumption_min = fields.Float(string="Max stiffness - Air consumption min.")
    max_stiffness_air_consumption_max = fields.Float(string="Max stiffness - Air consumption max.")

    # airc_airbe data
    mounting_kit_id = fields.Many2one("product.template", string="Mounting Kit")
    product_kit_ids = fields.One2many('product.template', 'mounting_kit_id', string='Perfect fit for')
    wiper_kit_id = fields.Many2one("product.template", string="Wiper Kit")
    rfx_id = fields.Many2one("product.template", string="Air bushing + support version")
    screw_pin_thread = fields.Char(string="Screw pin / Thread")
    air_nominal_supply_pressure = fields.Float(string="Nominal air supply pressure")
    product_load = fields.Float(string="Load")
    max_stiffness_load = fields.Float(string="Max stiffness - Load")
    stiffness = fields.Float(string="Stiffness")
    max_stiffness = fields.Float(string="Maximum stiffness")
    air_gap = fields.Float(string="Air gap")

    # dimension data
    length = fields.Float(string="Length")
    packing_weight = fields.Float(string="Packing Weight")
    width = fields.Float(string="Width")
    height = fields.Float(string="Height")
    diameter = fields.Float(string="Diameter")
    length_uom_name = fields.Char(string='Height unit of measure label', compute='_compute_length_uom_name')
    rbb_dimensions = fields.Char(string="Rbb Dimensions")

    # airc_airbe_hra variants data
    hra_interfacing = fields.Many2one("accessories", string="Methods of Interfacing")
    hra_coating_air_surface = fields.Many2one("accessories", string="Coatings aerostatic surface")
    dimensions_descriptions = fields.Char(string="Dimensions and Descriptions")

    # other products data
    perfect_fit_for_others = fields.Char(string="Perfect fit for")

    @api.depends('name')
    def _compute_length_uom_name(self):
        self.length_uom_name = self._get_length_uom_name_from_ir_config_parameter()

    @api.depends('series')
    def _compute_support(self):
        for record in self:
            if record.series != "xab":
                record.support = False

    @api.depends('display_category_id')
    def _compute_series_type(self):
        for record in self:
            if not record.display_category_id:
                return
            series = ['hpr', 'hpc', 'hra', 'xab', 'kit', 'other']
            for serie in series:
                if serie in record.display_category_id.complete_name.lower():
                    record.series = serie
                    break
