from odoo import fields,models,api,_
from datetime import datetime,date
from odoo.exceptions import ValidationError,UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
import calendar

class BonusForm(models.Model):
    _name = 'bonus.form'

    from_date = fields.Date(required=True)
    to_date = fields.Date(required=True)
    bonus_lines = fields.One2many('bonus.lines','bonus_formid')




    def payment(self):
        if self.bonus_lines:
            count = 1
            for line in self.bonus_lines:
                if line.select == True:
                    if line.payment_type:
                        count += 1
                        line.commission_id.status = 'paid'
                        line.commission_id.payment_date = datetime.now().date()
                        # First Entry
                        journal_list = []
                        journal_line2 = (0, 0, {
                            'account_id': self.env['account.account'].search([('name', '=', 'Salary Expenses')]).id,
                            'partner_id': line.employee_id.address_home_id.id,
                            'name': 'Weekly Bonus',
                            'debit': line.commission,
                        })
                        journal_list.append(journal_line2)
                        journal_line1 = (0, 0, {
                            'account_id': self.env['account.account'].search([('name', '=', 'Wages Payable')]).id,
                            'partner_id': line.employee_id.address_home_id.id,
                            'name': 'Weekly Bonus',
                            'credit': line.commission,
                        })
                        journal_list.append(journal_line1)
                        journal_id = self.env['account.move'].create({
                            'date': datetime.now().date(),
                            'ref': 'Weekly Bonus',
                            'journal_id': self.env['account.journal'].search(
                                [('name', '=', 'Miscellaneous Operations')]).id,
                            'line_ids': journal_list,
                        })
                        journal_id.action_post()





                        # Second Entry

                        if line.payment_type.name == 'Cash':
                            payment_id = self.env['account.account'].search([('name','=','Cash')]).id
                        else:
                            payment_id = self.env['account.account'].search([('name', '=', 'Bank')]).id
                        journal_list = []
                        journal_line3 = (0, 0, {
                            'account_id': self.env['account.account'].search([('name', '=', 'Wages Payable')]).id,
                            'partner_id': line.employee_id.address_home_id.id,
                            'name': 'Weekly Bonus',
                            'debit': line.commission,
                        })
                        journal_list.append(journal_line3)
                        journal_line4 = (0, 0, {
                            'account_id': payment_id,
                            'partner_id': line.employee_id.address_home_id.id,
                            'name': 'Weekly Bonus',
                            'credit': line.commission,
                        })
                        journal_list.append(journal_line4)
                        journal_id_2 = self.env['account.move'].create({
                            'date': datetime.now().date(),
                            'ref': 'Weekly Bonus',
                            'journal_id': line.payment_type.id,
                            'line_ids': journal_list,
                        })
                        journal_id_2.action_post()


            if count == 0:
                raise ValidationError(_(
                    'Please Select A Record'))
        else:
            raise ValidationError(_(
                'Nothing to Pay'))
        self.compute_bonus_lines()

    @api.onchange('from_date','to_date')
    def compute_bonus_lines(self):
        if self.from_date:
            if self.to_date:
                bonus_details = self.env['bonus.rec'].search([('status','=','unpaid'),('date','>=',self.from_date),('date','<=',self.to_date)])
                bonus_list = []
                for line in bonus_details:
                    details = (0,0,{
                        'employee_id':line.employee_id.id,
                        'date':line.date,
                        'commission':line.commission,
                        'status':line.status,
                        'commission_id':line.id
                    })
                    bonus_list.append(details)
                self.bonus_lines = None
                self.bonus_lines = bonus_list



class BonusLines(models.Model):
    _name = 'bonus.lines'

    bonus_formid = fields.Many2one('bonus.form')
    employee_id = fields.Many2one('hr.employee')
    date = fields.Date('Created Date')
    commission = fields.Float(string='Bonus Amount')
    payment_type = fields.Many2one('account.journal', string='Payment Type', domain=[('type', 'in', ('bank', 'cash'))])
    select = fields.Boolean()
    status = fields.Selection([('unpaid', 'Unpaid'), ('paid', 'Paid')])
    commission_id = fields.Many2one('bonus.rec')