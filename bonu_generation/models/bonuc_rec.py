from odoo import fields, models
from datetime import datetime, date
from odoo.exceptions import ValidationError, UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
import calendar


class Employee(models.Model):
    _inherit = "hr.employee"

    def weeklybonus(self):
        date = datetime.now().date().strftime(DEFAULT_SERVER_DATE_FORMAT)
        born = datetime.strptime(date, '%Y-%m-%d').weekday()
        day_name =  (calendar.day_name[born])
        days = self.env['bonus.config'].search([])
        for details in days:
            if day_name == details.name:
                employee_ids = self.env['hr.employee'].search([])
                for line in employee_ids:
                    contract_ids = self.env['hr.contract'].search([('employee_id', '=', line.id), ('state', '=', 'open')])
                    if contract_ids:
                        self.env['bonus.rec'].create({
                            'employee_id':line.id,
                            'date':datetime.now().date().strftime(DEFAULT_SERVER_DATE_FORMAT),
                            'commission':details.bonus,
                            'status':'unpaid',
                        })


class BonusRec(models.Model):
    _name = 'bonus.rec'

    employee_id = fields.Many2one('hr.employee')
    date = fields.Date(default=datetime.now().date().strftime(DEFAULT_SERVER_DATE_FORMAT))
    commission = fields.Float(string='Bonus Amount')
    status = fields.Selection([('unpaid', 'Unpaid'), ('paid', 'Paid')])
    payment_date = fields.Date()


class BonusConfig(models.Model):
    _name = 'bonus.config'

    name = fields.Selection([('Monday','Monday'),('Tuesday','Tuesday'),('Wednesday','Wednesday'),('Thursday','Thursday'),('Friday','Friday'),('Saturday','Saturday'),('Sunday','Sunday')])
    bonus = fields.Float('Bonus Amount')