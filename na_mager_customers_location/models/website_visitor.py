# -- coding: utf-8 --
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models, _
from odoo.http import request as odoo_request
import requests
from psycopg2 import sql


class WebsiteVisitor(models.Model):
    _inherit = 'website.visitor'

    def get_country_id(self):
        # request the data from the url
        url = 'http://ipinfo.io/json'
        request = requests.get(url)
        json_data = request.json()

        if not odoo_request:
            # get the country
            country_code = json_data['country']
        else:
            country_code = odoo_request.geoip.get('country_code')
        country_id = self.env['res.country'].search([
            ('code', '=', country_code)], limit=1)

        return country_id

    def _upsert_visitor(self, access_token, force_track_values=None):
        visitor_id, upsert = super()._upsert_visitor(access_token, force_track_values=force_track_values)
        country_id = self.get_country_id()
        last_create = self.env['website.visitor'].search([('access_token', '=', access_token)],
                                                         order='create_date desc', limit=1)
        if not last_create:
            return False
        last_create.write({
            'country_id': country_id.id,
        })
        return visitor_id, upsert

    # def _upsert_visitor(self, access_token, force_track_values=None):
    #     country_id = self.get_country_id()
    #
    #     create_values = {
    #         'access_token': access_token,
    #         'lang_id': request.lang.id,
    #         'country_id': country_id,
    #         'website_id': request.website.id,
    #         'timezone': self._get_visitor_timezone() or None,
    #         'write_uid': self.env.uid,
    #         'create_uid': self.env.uid,
    #         # If the access_token is not a 32 length hexa string, it means that the
    #         # visitor is linked to a logged in user, in which case its partner_id is
    #         # used instead as the token.
    #         'partner_id': None if len(str(access_token)) == 32 else access_token,
    #     }
    #
    #     query = """
    #         INSERT INTO website_visitor (
    #             partner_id, access_token, last_connection_datetime, visit_count, lang_id,
    #             country_id, website_id, timezone, write_uid, create_uid, write_date, create_date)
    #         VALUES (
    #             %(partner_id)s, %(access_token)s, now() at time zone 'UTC', 1, %(lang_id)s,
    #             %(country_id)s, %(website_id)s, %(timezone)s, %(create_uid)s, %(write_uid)s,
    #             now() at time zone 'UTC', now() at time zone 'UTC')
    #         ON CONFLICT (access_token)
    #         DO UPDATE SET
    #             last_connection_datetime=excluded.last_connection_datetime,
    #             visit_count = CASE WHEN website_visitor.last_connection_datetime < NOW() AT TIME ZONE 'UTC' - INTERVAL '8 hours'
    #                                 THEN website_visitor.visit_count + 1
    #                                 ELSE website_visitor.visit_count
    #                             END
    #         RETURNING id, CASE WHEN create_date = now() at time zone 'UTC' THEN 'inserted' ELSE 'updated' END AS upsert
    #     """
    #
    #     if force_track_values:
    #         create_values['url'] = force_track_values['url']
    #         create_values['page_id'] = force_track_values.get('page_id')
    #         query = sql.SQL("""
    #             WITH visitor AS (
    #                 {query}, %(url)s AS url, %(page_id)s AS page_id
    #             ), track AS (
    #                 INSERT INTO website_track (visitor_id, url, page_id, visit_datetime)
    #                 SELECT id, url, page_id::integer, now() at time zone 'UTC' FROM visitor
    #             )
    #             SELECT id, upsert from visitor;
    #         """).format(query=sql.SQL(query))
    #
    #     self.env.cr.execute(query, create_values)
    #     return self.env.cr.fetchone()
