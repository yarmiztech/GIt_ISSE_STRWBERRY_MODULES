from odoo import fields,models,_,api
from datetime import datetime,date
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class Contract(models.Model):
    _inherit = 'hr.contract'

    offer_id = fields.Many2one('offer.letter')


class OfferLetter(models.Model):
    _name = 'offer.letter'

    name = fields.Many2one('res.partner')
    department_id = fields.Many2one('hr.department')
    job_id = fields.Many2one('hr.job')
    last_joining_date = fields.Date()
    salary = fields.Float('Salary(Per Year)')
    date = fields.Date(default=datetime.now().date().strftime(DEFAULT_SERVER_DATE_FORMAT))
    join_date = fields.Date()
    states = fields.Selection([('draft','Draft'),('joined','Joined'),('mark as employee','Mark As Employee'),('contract Created','Contract Created'),('cancel','Cancel')],default='draft',compute='check_status')
    emp_count = fields.Integer(compute='employee_count')
    contract_count = fields.Integer(compute='compute_contract_count')

    def cancel(self):
        self.write({'states':'cancel'})

    def employee_count(self):
        for line in self:
            line.emp_count = len(self.env['hr.employee'].search([('offer_id','=',line.id)]))
    def compute_contract_count(self):
        for line in self:
            line.contract_count = len(self.env['hr.contract'].search([('offer_id','=',line.id)]))

    @api.depends('emp_count','contract_count')
    def check_status(self):
        for line in self:
            if not line.join_date:
                line.states = 'draft'
            if line.join_date:
                line.states = 'joined'
            if line.emp_count > 0:
                line.states = 'mark as employee'
            if line.contract_count > 0:
                line.states = 'contract Created'


    def compute_states(self):
        for line in self:
            if line.employee_count > 0:
                line.states = 'mark as employee'
            if line.contract_count > 0:
                line.states = 'contract Created'

    def commited(self):
        self.write({'states':'joined'})
        self.join_date = datetime.now().date().strftime(DEFAULT_SERVER_DATE_FORMAT)


    def employee_details(self):
        return {
            'name': _('Employee Details'),
            'view_type': 'form',
            'domain': [('offer_id', '=', self.id)],
            'res_model': 'hr.employee',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def contract_details(self):
        return {
            'name': _('Contract Details'),
            'view_type': 'form',
            'domain': [('offer_id', '=', self.id)],
            'res_model': 'hr.contract',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }


    def emp_registration(self):
        return {
            'name': _('Employee Registration'),
            'view_type': 'form',
            'res_model': 'hr.employee',
            'view_id': False,
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'context': {
                'default_offer_id': self.id,
                'default_department_id':self.department_id.id,
                'default_job_id':self.job_id.id,
                'default_address_home_id':self.name.id,
                'default_name':self.name.name,
            }
        }

    def contract_creation(self):
        return {
            'name': _('Contract Creation'),
            'view_type': 'form',
            'res_model': 'hr.contract',
            'view_id': False,
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'context': {
                'default_offer_id': self.id,
                'default_wage': self.salary / 12,
            }
        }