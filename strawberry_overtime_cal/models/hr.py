from odoo import fields,models,api,_
from odoo.tests.common import Form
from datetime import datetime
from odoo.exceptions import UserError, ValidationError

class Employee(models.Model):
    _inherit = "hr.employee"

    overtime_monthly = fields.Float(string='OT Monthly(Value)')
    overtime_hrs = fields.Float(string='OT Duration(Hrs)')


class Contract(models.Model):
    _inherit = 'hr.contract'

    overtime_monthly = fields.Float(string='OT Monthly(Value)')
    overtime_hrs = fields.Float(string='OT Duration(Hrs)')
