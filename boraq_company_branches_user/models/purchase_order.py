from odoo import api, fields, models, tools, _


class ResUsers(models.Model):
    _inherit = "res.users"

    branch_id = fields.Many2one('company.branches')
