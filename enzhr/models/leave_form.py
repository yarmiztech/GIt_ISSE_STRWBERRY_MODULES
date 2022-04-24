from odoo import fields,models,api
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT


class LeaveForm(models.Model):
    _name = 'leave.form'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char('Description')
    date = fields.Date(default=datetime.now().date().strftime(DEFAULT_SERVER_DATE_FORMAT),string='Created Date')
    employee_id = fields.Many2one('hr.employee')
    holiday_status_id = fields.Many2one('hr.leave.type',string='Leave Type')
    request_date_from_first = fields.Date('From Date')
    request_date_to_first = fields.Date('To date')
    request_date_from = fields.Date('Form Date')
    request_date_to = fields.Date('To Date')
    number_of_days_first = fields.Float(compute='compute_days_first',string='Number Of days Requested')
    number_of_days = fields.Float(compute='compute_days',string='Number Of Days Approved')
    status = fields.Selection([('draft','Draft'),('submit','Submit'),('approved','Approved'),('rejected','Rejected')],default='draft')

    @api.onchange('request_date_from_first')
    def check_todate(self):
        if self.request_date_from_first:
            self.request_date_to_first = self.request_date_from_first

    @api.onchange('request_date_from')
    def check_approve_date(self):
        if self.request_date_from:
            self.request_date_to = self.request_date_from


    def rejected_request(self):
        if self.request_date_from_first:
            if self.request_date_to_first:
                if self.employee_id:
                    if self.holiday_status_id:
                        self.status = 'rejected'

    @api.depends('request_date_from_first','request_date_to_first')
    def compute_days_first(self):
        for line in self:
            if line.request_date_from_first:
                if line.request_date_to_first:
                    if line.request_date_to_first == line.request_date_from_first:
                        line.number_of_days_first = 1
                    else:
                        delta = line.request_date_to_first - line.request_date_from_first
                        line.number_of_days_first = delta.days + 1
                else:
                    line.number_of_days_first = 0
            else:
                line.number_of_days_first = 0

    @api.depends('request_date_from','request_date_to')
    def compute_days(self):
        for line in self:
            if line.request_date_from:
                if line.request_date_to:
                    if line.request_date_to == line.request_date_from:
                        line.number_of_days = 1
                    else:
                        delta = line.request_date_to - line.request_date_from
                        line.number_of_days = delta.days + 1
                else:
                    line.number_of_days = 0
            else:
                line.number_of_days = 0

    def submit_request(self):
        if self.request_date_from_first:
            if self.request_date_to_first:
                if self.employee_id:
                    if self.holiday_status_id:
                        self.status = 'submit'

    def approve_request(self):
        if self.request_date_from:
            if self.request_date_to:
                if self.employee_id:
                    if self.holiday_status_id:
                        leaves = self.env[('hr.leave')].create({
                            'holiday_status_id': self.holiday_status_id.id,
                            'number_of_days': self.number_of_days,
                            'date_from': self.request_date_from,
                            'request_date_from': self.request_date_from,
                            'date_to': self.request_date_to,
                            'request_date_to': self.request_date_to,
                            'name': 'Personal',
                            'holiday_type': 'employee',
                            'employee_id': self.employee_id.id,
                            'department_id': self.employee_id.department_id.id,
                        })
                        leaves.action_approve()
                        self.status = 'approved'



