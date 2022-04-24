from odoo import fields,models
from datetime import datetime,date
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class WarningForm(models.Model):
    _name = 'warning.form'

    name = fields.Many2one('hr.employee')
    remark = fields.Text()
    date = fields.Date(default=datetime.now().date().strftime(DEFAULT_SERVER_DATE_FORMAT))
    state = fields.Selection([('draft','Draft'),('approve','Approve')])

    def approve_warning(self):
        self.write({'state':'approve'})