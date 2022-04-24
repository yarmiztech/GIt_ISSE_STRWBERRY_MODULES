from odoo import fields,models,api,_
from odoo.exceptions import ValidationError,UserError

class HrLoanChange(models.Model):
    _name = 'hr.loan.change'

    employee_id = fields.Many2one('hr.employee')
    loan_id = fields.Many2one('hr.loan')
    installment = fields.Integer()
    payment_lines = fields.One2many('hr.loan.payment.lines','loan_id')
    loan_amount = fields.Float()
    loan_flag = fields.Boolean()

    def update_loan(self):
        amount = 0
        for amount_lines in self.payment_lines:
            amount = amount + amount_lines.amount
        if amount != self.loan_amount:
            raise ValidationError(_(
                'Loan Amount Mismatch'))
        else:
            loan_list = []
            for lines in self.payment_lines:
                line = (0, 0, {
                    'date': lines.payment_date,
                    'amount': lines.amount,
                    'paid': lines.paid,
                })
                loan_list.append(line)
            self.loan_id.loan_lines = None
            self.loan_id.installment = len(self.payment_lines)
            self.loan_id.update({
                'loan_lines':loan_list
            })
            self.loan_flag = True
        self.installment = self.loan_id.installment

    @api.onchange('employee_id')
    def compute_payment_line(self):
        if self.employee_id:
            loan = self.env['hr.loan'].search([('employee_id','=',self.employee_id.id)])
            if loan.id:

                loan_list =[]
                for lines in loan.loan_lines:
                    line = (0,0,{
                        'payment_date':lines.date,
                        'amount':lines.amount,
                        'paid':lines.paid,
                    })
                    loan_list.append(line)
                self.payment_lines = None
                self.update({
                    'loan_id':loan.id,
                    'installment':loan.installment,
                    'payment_lines':loan_list,
                    'loan_amount':loan.loan_amount
                })
            else:
                raise ValidationError(_(
                    'No Loan available for this Employee'))

class LoanPaymentLines(models.Model):
    _name = 'hr.loan.payment.lines'

    loan_id = fields.Many2one('hr.loan.change')
    payment_date = fields.Date()
    amount = fields.Float()
    paid = fields.Boolean()

class HrLoan(models.Model):
    _inherit = 'hr.loan'

    def action_approve(self):
        # the inherited function for avoiding the checking of hr contract running or not
        self.write({'state': 'approve'})