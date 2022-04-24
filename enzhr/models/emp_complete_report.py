from odoo import fields, models, api


class EmployeeFullDetails(models.Model):
    _name = 'employee.full.details'
    _rec_name = 'employee_id'

    from_date = fields.Date()
    to_date = fields.Date()
    employee_id = fields.Many2one('hr.employee')
    job_id = fields.Many2one('hr.job')
    department_id = fields.Many2one('hr.department')
    visa_no = fields.Char()
    passport_no = fields.Char()
    resident_no = fields.Char()
    # visa_expiry = fields.Date()
    image = fields.Binary('Image')
    contract_lines = fields.One2many('contract.details', 'report_id')
    leave_lines = fields.One2many('leave.details', 'report_id')
    warning_lines = fields.One2many('warning.details', 'report_id')
    insurance_lines = fields.One2many('insurance.details', 'report_id')
    previous_lines = fields.One2many('previous.experiance', 'report_id')
    loan_lines = fields.One2many('loan.details', 'report_id')

    def print_employee_report(self):
        return self.env.ref('enzhr.employee_report_id').report_action(self)

    @api.onchange('employee_id')
    def compute_loans(self):
        if self.employee_id:
            loan_details = self.env['hr.loan'].search([('employee_id','=',self.employee_id.id),('state','=','approve')])
            loan_list = []
            for details in loan_details:
                line = (0,0,{
                    'name':details.name,
                    'loan_amount':details.loan_amount,
                    'total_paid_amount':details.total_paid_amount,
                    'balance_amount':details.balance_amount,
                    'date':details.date
                })
                loan_list.append(line)
            if loan_details:
                self.loan_lines = None
                self.loan_lines = loan_list

    @api.onchange('employee_id')
    def compute_experiance(self):
        if self.employee_id:
            experiance_details = self.env['previous.occupation'].search([('employee_id','=',self.employee_id.id)])
            previous_list = []
            for details in experiance_details:
                line = (0, 0, {
                    'from_date': details.from_date,
                    'to_date': details.to_date,
                    'position': details.position,
                    'organization': details.organization,
                    'ref_name': details.ref_name,
                    'ref_position': details.ref_position,
                    'ref_phone': details.ref_phone,
                })
                previous_list.append(line)
            if experiance_details:
                self.previous_lines = None
                self.previous_lines = previous_list

    @api.onchange('employee_id')
    def compute_values(self):
        if self.employee_id:
            self.job_id = self.employee_id.job_id.id
            self.department_id = self.employee_id.department_id.id
            self.visa_no = self.employee_id.visa_no
            self.passport_no = self.employee_id.passport_id
            self.resident_no = self.employee_id.resident_cardno

    @api.onchange('employee_id')
    def compute_insurance(self):
        if self.employee_id:
            if self.employee_id.insurance_lines:
                insurance_details = self.employee_id.insurance_lines
                insurance_list = []
                for details in insurance_details:
                    line = (0,0,{
                        'name':details.name,
                        'relation':details.relation,
                        'percentage':details.percentage,
                    })
                    insurance_list.append(line)
                if insurance_details:
                    self.insurance_lines = None
                    self.insurance_lines = insurance_list

    @api.onchange('employee_id')
    def compute_contract(self):
        if self.employee_id:
            # print(self.env['hr.contract'].search([('employee_id','=',self.employee_id.id),('date_start','<=',self.from_date)]))
            contract_details = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id)])
            contract_list = []
            for details in contract_details:
                line = (0, 0, {
                    'name': details.name,
                    'employee_id': details.employee_id.id,
                    'job_id': details.job_id.id,
                    # 'type_id': details.type_id.id,
                    'resource_calendar_id': details.resource_calendar_id.id,
                    'date_start': details.date_start,
                    'date_end': details.date_end,
                    'wage': details.wage,
                    'state': details.state
                })
                contract_list.append(line)
            if contract_details:
                self.contract_lines = None
                self.contract_lines = contract_list

    @api.onchange('employee_id')
    def compute_image(self):
        if self.employee_id:
            self.image = self.employee_id.image_1920

    @api.onchange('employee_id')
    def compute_leavedetails(self):
        if self.employee_id:
            leave_list = []
            leave_details = self.env['hr.leave'].search(
                [('employee_id', '=', self.employee_id.id), ('state', '=', 'validate')])
            for details in leave_details:
                line = (0, 0, {
                    'name': details.name,
                    'employee_id': details.employee_id.id,
                    'holiday_type': details.holiday_type,
                    'date_from': details.date_from,
                    'date_to': details.date_to,
                    'holiday_status_id': details.holiday_status_id.id,
                    'duration_display': details.duration_display
                })
                leave_list.append(line)
            if leave_details:
                self.leave_lines = None
                self.leave_lines = leave_list

    @api.onchange('employee_id')
    def compute_warnings(self):
        if self.employee_id:
            warning_details = self.env['warning.form'].search([('name','=',self.employee_id.id),('state','=','approve')])
            warning_list = []
            for details in warning_details:
                line = (0, 0, {
                    # 'name': details.name.id,
                    'remark': details.remark,
                    'date': details.date,
                })
                warning_list.append(line)
            if warning_details:
                self.warning_lines = None
                self.warning_lines = warning_list

class ContractDetails(models.Model):
    _name = 'contract.details'

    report_id = fields.Many2one('employee.full.details')
    name = fields.Char()
    employee_id = fields.Many2one('hr.employee')
    job_id = fields.Many2one('hr.job')
    # type_id = fields.Many2one('hr.contract.type')
    resource_calendar_id = fields.Many2one('resource.calendar')
    date_start = fields.Date()
    date_end = fields.Date()
    wage = fields.Float()
    state = fields.Selection([
        ('draft', 'New'),
        ('open', 'Running'),
        ('pending', 'To Renew'),
        ('close', 'Expired'),
        ('cancel', 'Cancelled')])


class LeaveDetails(models.Model):
    _name = 'leave.details'

    report_id = fields.Many2one('employee.full.details')
    employee_id = fields.Many2one('hr.employee')
    holiday_type = fields.Selection([
        ('employee', 'By Employee'),
        ('category', 'By Employee Tag')
    ], string='Allocation Mode')
    date_from = fields.Datetime('Start Date')
    date_to = fields.Datetime('End Date')
    holiday_status_id = fields.Many2one("hr.leave.type", string="Leave Type")
    name = fields.Char()
    duration_display = fields.Char()


class WarningDetails(models.Model):
    _name = 'warning.details'

    report_id = fields.Many2one('employee.full.details')
    name = fields.Many2one('hr.employee')
    remark = fields.Text()
    date = fields.Date()


class InsuranceDetails(models.Model):
    _name = 'insurance.details'

    report_id = fields.Many2one('employee.full.details')
    name = fields.Char()
    relation = fields.Char()
    percentage = fields.Float()

class PreviousExperiance(models.Model):
    _name = 'previous.experiance'

    report_id = fields.Many2one('employee.full.details')
    from_date = fields.Date()
    to_date = fields.Date()
    position = fields.Char()
    organization = fields.Char()
    ref_name = fields.Char()
    ref_position = fields.Char()
    ref_phone = fields.Char()

class LoanDetails(models.Model):
    _name = 'loan.details'

    report_id = fields.Many2one('employee.full.details')
    name = fields.Char()
    loan_amount = fields.Float()
    total_paid_amount = fields.Float()
    balance_amount = fields.Float()
    date = fields.Date()
