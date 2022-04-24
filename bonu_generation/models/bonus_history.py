from odoo import fields,models,api

class BonusPaymentHistory(models.Model):
    _name = 'bonus.payment.history'

    from_date = fields.Date(required=True)
    to_date = fields.Date(required=True)
    bonus_history_lines = fields.One2many('bonus.history.lines', 'bonus_formid')

    def bonus_report(self):
        return self.env.ref('bonu_generation.bonus_report').report_action(self)

    @api.onchange('from_date', 'to_date')
    def compute_history_lines(self):
        if self.from_date:
            if self.to_date:
                bonus_details = self.env['bonus.rec'].search(
                    [('status', '=', 'paid'), ('payment_date', '>=', self.from_date), ('payment_date', '<=', self.to_date)])
                bonus_list = []
                for line in bonus_details:
                    details = (0, 0, {
                        'employee_id': line.employee_id.id,
                        'date': line.date,
                        'commission': line.commission,
                        'status': line.status,
                        'commission_id': line.id,
                        'payment_date':line.payment_date
                    })
                    bonus_list.append(details)
                self.bonus_history_lines = None
                self.bonus_history_lines = bonus_list


class BonusHistoryLines(models.Model):
    _name = 'bonus.history.lines'

    bonus_formid = fields.Many2one('bonus.payment.history')
    employee_id = fields.Many2one('hr.employee')
    date = fields.Date('Created Date')
    commission = fields.Float(string='Bonus Amount')
    payment_date = fields.Date('Payment Date')
    # payment_type = fields.Many2one('account.journal', string='Payment Type', domain=[('type', 'in', ('bank', 'cash'))])
    # select = fields.Boolean()
    status = fields.Selection([('unpaid', 'Unpaid'), ('paid', 'Paid')])
    commission_id = fields.Many2one('bonus.rec')


