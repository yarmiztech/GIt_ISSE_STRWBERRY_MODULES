from odoo import models,fields,api
from datetime import datetime,timedelta,date
from dateutil.relativedelta import relativedelta

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

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
                        line.passport_allertcomp = False
            else:
                line.passport_allert = False
                line.passport_allertcomp = False

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
                        line.resident_card_allertcomp = False
            else:
                line.resident_card_allertcomp = False
                line.resident_card_allert = False

    def calculateage(self):
        for line in self.env['hr.employee'].search([]):
            if line.birthday:
                today = date.today()
                age = today.year - line.birthday.year - (
                            (today.month, today.day) < (line.birthday.month, line.birthday.day))
                print(age)
                line.emp_age = age
                alert_details = self.env['alert.config'].search([])
                for alert in alert_details:
                    age_conf = alert.age
                    if age > age_conf:
                        line.emp_age_allertcomp = True
                        line.emp_age_allert = True
                    else:
                        line.emp_age_allert = False
                        line.emp_age_allertcomp = False
            else:
                line.emp_age = 0
                line.emp_age_allertcomp = False
                line.emp_age_allert = False

