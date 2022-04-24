from odoo import fields,models,api,_
from datetime import datetime,timedelta,date
from dateutil.relativedelta import relativedelta

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # no_of_leaves = fields.Integer()
    passport_expiry = fields.Date()
    passport_allert = fields.Boolean()
    visa_alert = fields.Boolean()
    passport_allertcomp = fields.Boolean(compute='passport_expirycheck')
    resident_cardno = fields.Char(string='Resident Card No')
    resident_cardexp = fields.Date('Expiry Date')
    resident_card_allert = fields.Boolean()
    resident_card_allertcomp = fields.Boolean(compute='residentalert')
    emp_age = fields.Integer(compute='calculateage',string='Age')
    emp_age_allert = fields.Boolean()
    emp_age_allertcomp = fields.Boolean(compute='calculateage')
    offer_id = fields.Many2one('offer.letter')
    insurance_lines = fields.One2many('insurance.lines','employee_id')
    experiance_lines = fields.One2many('previous.occupation','employee_id')
    warning_count = fields.Integer(compute='warning_countcomp')

    # prevoius_exp = fields.Text()

    def warning_countcomp(self):
        for line in self:
            line.warning_count = len(self.env['warning.form'].search([('name','=',line.id)]))

    def warning(self):
        return {
            'name': _('Warning'),
            'view_type': 'form',
            'domain': [('name', '=', self.id), ('state', '=', 'approve')],
            'res_model': 'warning.form',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def experiance_certify(self):
        return {
            'name': _('Experiance Certificate'),
            'view_type': 'form',
            'domain': [('employee_id', '=', self.id),('status','=','approved')],
            'res_model': 'experience.certificate',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }



    def visaalert(self):
        for line in self.env['hr.employee'].search([]):
            if line.visa_expire:
                alert_details = self.env['alert.config'].search([])
                for alert in alert_details:
                    month = alert.visa_month
                    if date.today() > line.visa_expire - relativedelta(months=month):
                        line.visa_alert = True
                    else:
                        line.visa_alert = False

    # @api.depends('resident_cardexp')
    def residentalert(self):
        for line in self.env['hr.employee'].search([]):
            if line.resident_cardexp:
                alert_details = self.env['alert.config'].search([])
                for alert in alert_details:
                    month = alert.resident_month
                    if date.today() > line.resident_cardexp - relativedelta(months=month):
                        line.resident_card_allertcomp = True
                        line.resident_card_allert = True
                    else:
                        line.resident_card_allert = False
            else:
                line.resident_card_allertcomp = False
                line.resident_card_allert = False
    # @api.onchange('resident_card_allertcomp')
    # def selfcheckresidentalert(self):
    #     if self.resident_card_allertcomp == True:
    #         self.resident_card_allert = True


    # @api.depends('passport_expiry')
    def passport_expirycheck(self):
        for line in self.env['hr.employee'].search([]):
            if line.passport_expiry:
                alert_details = self.env['alert.config'].search([])
                for alert in alert_details:
                    month = alert.passport_month
                    if date.today() > line.passport_expiry - relativedelta(months=month):
                        line.passport_allertcomp = True
                        line.passport_allert = True
                    else:
                        line.passport_allert = False
            else:
                line.passport_allert = False
                line.passport_allertcomp = False

    # @api.onchange('passport_allertcomp')
    # def selfcheckpassport(self):
    #     if self.passport_allertcomp == True:
    #         self.passport_allert = True


    # @api.depends('birthday')
    def calculateage(self):
        for line in self.env['hr.employee'].search([]):
            if line.birthday:
                print(line.birthday)
                today = date.today()
                age = today.year - line.birthday.year -((today.month, today.day) < (line.birthday.month, line.birthday.day))
                line.emp_age = age
                alert_details = self.env['alert.config'].search([])
                for alert in alert_details:
                    age_conf = alert.age
                    if age > age_conf:
                        line.emp_age_allertcomp = True
                        line.emp_age_allert = True
                    else:
                        line.emp_age_allert = False
            else:
                line.emp_age = 0
                line.emp_age_allertcomp = False
                line.emp_age_allert = False

    # @api.onchange('emp_age_allertcomp')
    # def selfcheckage(self):
    #     if self.emp_age_allertcomp == True:
    #         self.emp_age_allert = True
    #         print('po1')

    # def calculateage():
    #     today = date.today()
    #     age = today.year - birthDate.year -
    #     ((today.month, today.day) <
    #      (birthDate.month, birthDate.day))
    #
    # return age

class InsuranceLines(models.Model):
    _name = 'insurance.lines'

    employee_id = fields.Many2one('hr.employee')
    name = fields.Char()
    relation = fields.Char()
    percentage = fields.Float()
