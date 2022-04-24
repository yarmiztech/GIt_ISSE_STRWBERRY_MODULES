# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64

from odoo import fields, api, models


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    # absolute_discount = fields.Float(string="Discount per Unit (abs)", default=0.0)
    ar_name = fields.Char(string="Arabic")

    @api.depends('full_product_name')
    @api.constrains('full_product_name')
    def _onchange_full_product_name(self):
        if self.full_product_name:
            # self.ar_name =self.full_product_name.ar_name
            self.ar_name =self.env['product.template'].search([('name','=',self.full_product_name)]).ar_name

    def enzapps_product_call(self):
        rec = self.env['product.product'].search([('id', '=', self.product_id.id)]).ar_name
        return rec

