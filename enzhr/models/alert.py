from odoo import fields,models

class AlertConfig(models.Model):
    _name = 'alert.config'

    name = fields.Char(default='Alert Configuration')
    visa_month = fields.Integer()
    resident_month = fields.Integer()
    passport_month = fields.Integer()
    age = fields.Integer()