# -- coding: utf-8 --
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import base64
import requests
import io
from PIL import Image

from odoo import api, fields, models, _


class BaseImport(models.TransientModel):
    _inherit = "base_import.import"

    def execute_import(self, fields, columns, options, dryrun=False):
        res = super(BaseImport, self).execute_import(fields, columns, options, dryrun=dryrun)
        if self.res_model == 'product.template':
            if not res['messages'] and not dryrun:
                for prod_name in res['name']:
                    product = self.env['product.template'].search([('name', '=', prod_name)])
                    # fixme [AMASTINI]: add an "try:except" and then tab
                    image_url = product[0].image
                    if not image_url:
                        return res

                    img = Image.open(image_url, mode='r')
                    img_byte_array = io.BytesIO()
                    img.save(img_byte_array, format='JPEG', subsampling=0, quality=100)
                    img_byte_array = img_byte_array.getvalue()

                    print(img_byte_array)

                    data = base64.b64encode(img_byte_array)

                    print(data)
                    product[0].image_1920 = data
        return res
