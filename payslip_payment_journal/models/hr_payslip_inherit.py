from odoo import fields,models,api

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    total_amount_journal = fields.Float(string='Total Amount', compute='compute_total_amount_journal', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('verify', 'Waiting'),
        ('done', 'Done'),
        ('cancel', 'Rejected'),
        ('paid', 'Paid'),
    ], string='Status', index=True, readonly=True, copy=False, default='draft',
        help="""* When the payslip is created the status is \'Draft\'
                    \n* If the payslip is under verification, the status is \'Waiting\'.
                    \n* If the payslip is confirmed then status is set to \'Done\'.
                    \n* When user cancel payslip the status is \'Rejected\'.""")


    @api.depends('line_ids')
    @api.onchange('line_ids')
    def compute_total_amount_journal(self):
        for slip in self:
            total_amount_new = 0.0
            for line in slip.line_ids:
                if line.salary_rule_id.code == 'NET':
                    total_amount_new += line.total

            slip.total_amount_journal = total_amount_new

