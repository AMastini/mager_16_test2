# -- coding: utf-8 --
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class MagerInvoice(models.Model):
    _name = "mager.invoice"
    _inherit = ['portal.mixin']
    _description = "Mager Documents"

    customer = fields.Many2one('res.partner', string='Customer')
    name = fields.Char(string='Name')
    date_of_issue = fields.Date(string='Date of Issue')
    invoice_due_date = fields.Date(string='Invoice Due Date')
    attachment = fields.Many2one('ir.attachment',
                                 string='Attachment')  # TODO: rename to attachment_id because it is a many2one field
    pdf_file = fields.Binary(related='attachment.datas', string='Download')
    file_name = fields.Char(related='attachment.name', string='PDF Name')
    pdf_link = fields.Char(string="Download or Print Link", compute="_compute_get_pdf_link", store=True)
    mager_invoice_count = fields.Integer(compute='_compute_mager_invoice_count', string='Mager Invoices Count')
    document_type = fields.Selection([('invoice', 'Invoice'), ('ddt', 'DDT')])

    @api.depends('attachment')
    def _compute_get_pdf_link(self):
        for custom_invoice in self:
            url = self.env['ir.config_parameter'].sudo().get_param(
                'web.base.url') + '/web/content/{}/{}'.format(
                custom_invoice.attachment.id,
                custom_invoice.attachment.name)
            custom_invoice.pdf_link = str(url).replace('(\'', '')

    def _compute_mager_invoice_count(self):
        mager_invoice_data = self.env['mager.invoice']._read_group(domain=[('pdf_link', '!=', False)],
                                                                   fields=['id'],
                                                                   groupby=['id'])
        mapped_data = dict([(m['id'][0], m['id']) for m in mager_invoice_data])
        for invoice in self:
            invoice.mager_invoice_count = mapped_data.get(invoice.id, 0)
