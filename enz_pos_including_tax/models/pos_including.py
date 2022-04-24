# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
# from datetime import datetime
# from datetime import date
# import time
# import fcntl
# import socket
# import struct
# import macpath
# from uuid import getnode as get_mac
# from odoo.exceptions import UserError, ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    including_price = fields.Float(string='Including Tax')

    @api.onchange('including_price')
    def _onchange_including_price(self):
        if self.including_price:
            print('frtgrtr')
            tax_value = self.including_price * 15 / (115)
            self.list_price = self.including_price - tax_value

