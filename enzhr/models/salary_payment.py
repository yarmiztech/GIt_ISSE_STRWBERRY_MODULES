from odoo import fields,models,api

class SalaryPaymentsHr(models.Model):
    _name = 'salary.payment.hr'

    department_id = fields.Many2one('hr.department')
    payment_lines = fields.One2many('salary.payment.lines.hr','salary_id')
    month = fields.Selection([('01','January'),('02','February'),('03','March'),('04','April'),('05','May'),('06','June'),('07','July'),('08','August'),('09','September'),('10','October'),('11','November'),('12','December')])
    payslip_flag = fields.Boolean()

    def payment(self):
        if self.payment_lines:
            for line in self.payment_lines:
                # print(line.payment_amount)
                journal_list = []
                journal_line2 = (0, 0, {
                    'account_id': self.env['account.account'].search([('name', '=', 'Salary Expenses')]).id,
                    # 'partner_id': line.employee_id.id,
                    'name': 'Salary Payment',
                    'debit': line.payment_amount,
                })
                journal_list.append(journal_line2)
                journal_line1 = (0, 0, {
                    'account_id': self.env['account.account'].search([('name', '=', 'Wages Payable')]).id,
                    # 'partner_id': line.employee_id.id,
                    'name': 'Salary Payment',
                    'credit': line.payment_amount,
                })
                journal_list.append(journal_line1)
                journal_id = self.env['account.move'].create({
                    'date': line.date,
                    'ref': line.description,
                    'journal_id': self.env['account.journal'].search(
                        [('name', '=', 'Miscellaneous Operations')]).id,
                    'line_ids': journal_list,
                })
                journal_id.action_post()

                if line.payment_type.name == 'Cash':
                    payment_id = self.env['account.account'].search([('name', '=', 'Cash')]).id
                else:
                    payment_id = self.env['account.account'].search([('name', '=', 'Bank')]).id

                journal_list_1 = []
                journal_line_two = (0, 0, {
                    'account_id': self.env['account.account'].search([('name', '=', 'Wages Payable')]).id,
                    # 'partner_id': line.employee_id.id,
                    'name': 'Salary Payment',
                    'debit': line.payment_amount,
                })
                journal_list_1.append(journal_line_two)
                journal_line_one = (0, 0, {
                    'account_id': payment_id,
                    # 'partner_id': line.employee_id.id,
                    'name': 'Salary Payment',
                    'credit': line.payment_amount,
                })
                journal_list_1.append(journal_line_one)
                journal_id_1 = self.env['account.move'].create({
                    'date': line.date,
                    'ref': line.description,
                    'journal_id': line.payment_type.id,
                    'line_ids': journal_list_1,
                })
                journal_id_1.action_post()
            self.payslip_flag = True

    @api.onchange('department_id')
    def compute_payment_lines(self):
        if self.department_id:
            contract_ids = self.env['hr.contract'].search([('department_id','=',self.department_id.id),('state', 'not in', ('close', 'cancel'))])
            pay_list = []
            for line in contract_ids:
                list_line = (0,0,{
                    'employee_id':line.employee_id.id,
                    # 'external_emp':line.external_emp,
                    'basic_salary':line.wage,
                    'payment_type':self.env['account.journal'].search([('name','=','Cash')])
                })
                pay_list.append(list_line)
            self.payment_lines = None
            self.payment_lines = pay_list


class SalaryPaymentLinesHr(models.Model):
    _name = 'salary.payment.lines.hr'

    salary_id = fields.Many2one('salary.payment.hr')
    employee_id = fields.Many2one('hr.employee')
    month = fields.Selection([('01','January'),('02','February'),('03','March'),('04','April'),('05','May'),('06','June'),('07','July'),('08','August'),('09','September'),('10','October'),('11','November'),('12','December')])
    basic_salary = fields.Float()
    payment_type = fields.Many2one('account.journal', string='Payment Types', domain=[('type', 'in', ('bank', 'cash'))])
    date = fields.Date()
    payment_amount = fields.Float()
    description = fields.Char()
    deduction = fields.Float()


    @api.onchange('basic_salary','deduction')
    def compute_payment_amt(self):
        if self.basic_salary:
            if self.deduction:
                self.payment_amount = self.basic_salary - self.deduction