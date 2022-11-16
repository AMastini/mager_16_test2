# -- coding: utf-8 --
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.http import request
from odoo.exceptions import AccessError, MissingError


class PortalAccount(CustomerPortal):

    @http.route(['/my/mager_invoices', '/my/mager_invoices/page/<int:page>'], type='http', auth="user", website=True)
    def portal_mager_my_invoices(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_mager_my_invoices_values(page, date_begin, date_end, sortby, filterby)

        # pager
        pager = portal_pager(**values['pager'])

        # content according to pager and archive selected
        invoices = values['invoices'](pager['offset'])
        request.session['my_invoices_history'] = invoices.ids[:100]  # TODO: check "page" and "pager" usage

        invoices = self.filtered_documents('invoice', invoices)

        values.update({
            'page_name': 'mager_invoice',
            'invoices': invoices,
            'pager': pager,
        })
        return request.render("na_mager_invoice.portal_mager_my_invoices", values)

    @http.route(['/my/mager_ddts', '/my/mager_ddts/page/<int:page>'], type='http', auth="user", website=True)
    def portal_mager_my_ddts(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_mager_my_ddts_values(page, date_begin, date_end, sortby, filterby)

        # pager
        pager = portal_pager(**values['pager'])

        # content according to pager and archive selected
        invoices = values['invoices'](pager['offset'])
        request.session['my_invoices_history'] = invoices.ids[:100]  # TODO: check "page" and "pager" usage

        invoices = self.filtered_documents('ddt', invoices)

        values.update({
            'page_name': 'mager_ddt',
            'invoices': invoices,
            'pager': pager,
        })
        return request.render("na_mager_invoice.portal_mager_my_ddts", values)

    @http.route(['/my/mager_invoices/<int:id>'], type='http', auth="public", website=True)
    def portal_my_mager_invoice_detail(self, id, access_token=None, report_type=None):
        try:
            invoice_sudo = self._document_check_access('mager.invoice', id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=invoice_sudo, report_type='pdf', report_ref='mager.invoice',
                                     download=True)

        return self._show_report(model=invoice_sudo, report_type='pdf', report_ref='mager.invoice',
                                 download=True)

    @http.route(['/my/mager_ddts/<int:id>'], type='http', auth="public", website=True)
    def portal_my_mager_ddts_detail(self, id, access_token=None, report_type=None):
        try:
            invoice_sudo = self._document_check_access('mager.invoice', id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=invoice_sudo, report_type='pdf', report_ref='mager.invoice',
                                     download=True)

        return self._show_report(model=invoice_sudo, report_type='pdf', report_ref='mager.invoice',
                                 download=True)

    def _prepare_mager_my_invoices_values(self, page, sortby, filterby, domain=None, url="/my/mager_invoices"):
        values = self._prepare_portal_layout_values()
        MagerInvoice = request.env['mager.invoice']

        domain = self._get_mager_invoices_domain()

        values.update({
            # content according to pager and archive selected
            # lambda function to get the invoices recordset when the pager will be defined in the main method of a route
            'invoices': lambda pager_offset: MagerInvoice.search(domain, limit=self._items_per_page,
                                                                 offset=pager_offset),
            'page_name': 'invoice',
            'pager': {  # vals to define the pager.
                "url": url,
                "total": MagerInvoice.search_count(domain),
                "page": page,
                "step": self._items_per_page,
            },
            'default_url': url,
        })
        return values

    def _prepare_mager_my_ddts_values(self, page, sortby, filterby, domain=None, url="/my/mager_ddts"):
        values = self._prepare_portal_layout_values()
        MagerInvoice = request.env['mager.invoice']

        domain = self._get_mager_invoices_domain()

        values.update({
            # content according to pager and archive selected
            # lambda function to get the invoices recordset when the pager will be defined in the main method of a route
            'invoices': lambda pager_offset: MagerInvoice.search(domain, limit=self._items_per_page,
                                                                 offset=pager_offset),
            'page_name': 'mager_ddt',
            'pager': {  # vals to define the pager.
                "url": url,
                "total": MagerInvoice.search_count(domain),
                "page": page,
                "step": self._items_per_page,
            },
            'default_url': url,
        })
        return values

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        mager_invoice_count = 0
        mager_ddt_count = 0
        mager_invoices = request.env['mager.invoice'].search([])
        if 'mager_invoice_count' in counters:
            mager_invoice_count = len(
                self.filtered_documents('invoice', mager_invoices)) \
                if request.env['mager.invoice'].check_access_rights('read', raise_exception=False) else 0
            values['mager_invoice_count'] = mager_invoice_count
        if 'mager_ddt_count' in counters:
            mager_ddt_count = len(self.filtered_documents('ddt', mager_invoices)) \
                if request.env['mager.invoice'].check_access_rights('read', raise_exception=False) else 0
            values['mager_ddt_count'] = mager_ddt_count
        return values

    def _get_mager_invoices_domain(self):
        return [('pdf_link', '!=', False)]

    def customer_invoices_filter(self, invoices):
        current_user = request.env['website.visitor']._get_visitor_from_request().partner_id

        customer_invoices = request.env['mager.invoice']
        if not current_user.user_has_groups('na_mager_product.product_group_manager_mager'):
            for invoice in invoices:
                if invoice.customer == current_user:
                    customer_invoices += invoice
                invoices = customer_invoices
            # fixme [MPAGANI]: use filtered
            # invoices = invoices.filtered(lambda inv: inv.customer == current_user)
        return invoices

    def filtered_documents(self, filter, documents):
        return self.customer_invoices_filter(documents).filtered(lambda inv: inv.document_type == filter)
