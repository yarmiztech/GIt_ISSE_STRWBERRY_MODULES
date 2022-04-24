from odoo import fields,models
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

class RegisterPaymentWizardJournal(models.Model):
    _name = 'register.payment.wizard.journal'

    employee_id = fields.Many2one('hr.employee')
    payment_type = fields.Many2one('account.journal', string='Payment Types', domain=[('type', 'in', ('bank', 'cash'))])
    amount = fields.Float()
    payment_date = fields.Date(default=datetime.now().date().strftime(DEFAULT_SERVER_DATE_FORMAT))
    communication = fields.Char()
    payslip_id = fields.Many2one('hr.payslip')

    def payment(self):
        if self.employee_id:
            partner_id = self.env['hr.employee'].search([('id','=',self.employee_id.id)]).address_home_id.id
            if self.payslip_id:
                if self.payment_type.name == 'Cash':
                    payment_id = self.env['account.account'].search([('name','=','Cash')]).id
                else:
                    payment_id = self.env['account.account'].search([('name', '=', 'Bank')]).id
                journal_list = []
                journal_line2 = (0, 0, {
                    'account_id': self.env['account.account'].search([('name', '=', 'Wages Payable')]).id,
                    'partner_id': partner_id,
                    'name': 'Net Salary',
                    'debit': self.amount,
                })
                journal_list.append(journal_line2)
                journal_line1 = (0, 0, {
                    'account_id': payment_id,
                    'partner_id': partner_id,
                    'name': 'Net Salary',
                    'credit': self.amount,
                })
                journal_list.append(journal_line1)
                journal_id = self.env['account.move'].create({
                    'date': datetime.now().date(),
                    'ref': self.payslip_id.number,
                    'journal_id': self.payment_type.id,
                    'line_ids': journal_list,
                })
                journal_id.action_post()
                self.payslip_id.state = 'paid'
            # count = 1
            # for line in self.commission_lines:
            #     if line.select == True:
            #         count += 1
            #         line.commission_id.status = 'paid'
            #         if line.payment_type.name == 'Cash':
            #             payment_id = self.env['account.account'].search([('name','=','Cash')]).id
            #         else:
            #             payment_id = self.env['account.account'].search([('name', '=', 'Bank')]).id
            #         journal_list = []
            #         journal_line2 = (0, 0, {
            #             'account_id': self.env['account.account'].search([('name', '=', 'Wages Payable')]).id,
            #             'partner_id': line.employee_id.id,
            #             'name': 'Daily Wage(Commission)',
            #             'debit': line.commission,
            #         })
            #         journal_list.append(journal_line2)
            #         journal_line1 = (0, 0, {
            #             'account_id': payment_id,
            #             'partner_id': line.employee_id.id,
            #             'name': 'Daily Wage(Commission)',
            #             'credit': line.commission,
            #         })
            #         journal_list.append(journal_line1)
            #         journal_id = self.env['account.move'].create({
            #             'date': datetime.now().date(),
            #             'ref': 'Daily Wage(Commission)',
            #             'journal_id': line.payment_type.id,
            #             'line_ids': journal_list,
            #         })
            #         journal_id.action_post()