from odoo import fields,models,api
from odoo.exceptions import UserError, ValidationError
class ExperienceCertificate(models.Model):
    _name = 'experience.certificate'

    employee_id = fields.Many2one('hr.employee')
    department_id = fields.Many2one('hr.department')
    job_id = fields.Many2one('hr.job')
    from_date = fields.Date()
    to_date = fields.Date()
    private_address = fields.Many2one('res.partner')
    remarks = fields.Text()
    status = fields.Selection([('draft','Draft'),('approved','Approved'),('rejected','Rejected')],default='draft')


    def rejected_certificate(self):
        if self.employee_id:
            self.status = 'rejected'

    def approve_certificate(self):
        if self.employee_id:
            self.status = 'approved'

    @api.onchange('employee_id')
    def compute_values(self):
        if self.employee_id:
            if self.env['hr.contract'].search([('employee_id','=',self.employee_id.id)]):
                contract_details = self.env['hr.contract'].search([('employee_id','=',self.employee_id.id)])[-1]
                if contract_details:
                    self.department_id = contract_details.department_id.id
                    self.job_id = contract_details.job_id.id
                    self.from_date = contract_details.date_start
                    self.to_date = contract_details.date_end
                    self.private_address = contract_details.employee_id.address_home_id.id
            else:
                raise ValidationError('No Contract Found For this employee')