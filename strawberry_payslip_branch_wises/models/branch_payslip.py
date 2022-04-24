from odoo import fields,models,api,_
from odoo.tests.common import Form
from datetime import datetime
from odoo.exceptions import UserError, ValidationError

class BranchPayslip(models.Model):
    _name = 'branch.payslip'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']




    name = fields.Char("Name", index=True, default=lambda self: _('New'))

    branch_id = fields.Many2one('company.branches', 'Branch Name')
    create_date = fields.Date(string='Create Date', default=fields.Date.context_today)

    user_id = fields.Many2one('res.users', 'Created By', required=True, default=lambda self: self.env.user)

    state = fields.Selection([('draft', 'Draft'), ('validate', 'Validate'), ('cancelled', 'Cancelled')], readonly=True,default='draft')
    straw_expense_lines = fields.One2many('branch.payslip.lines','branch_payslip_id')
    payslip_ids = fields.One2many('hr.payslip','payslip_id')
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.company)
    date_from = fields.Date(string='Date from')
    date_to = fields.Date(string='Date To')

    def action_journal_invoices(self):
        return {
            'name': _('Payslips'),
            'view_mode': 'tree,form',
            'res_model': 'hr.payslip',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.payslip_ids.ids)],
        }



    def action_confirm(self):
        for line in self.straw_expense_lines:
            vals = {
                'employee_id': line.hr_employee.id,
                'date_from': self.date_from,
                'date_to': self.date_to,
                'journal_id': line.journal_id.id,
                'payslip_id':self.id,
                'branch_id':self.branch_id.id,
            }
            hr_payslip = self.env['hr.payslip'].create(vals)
            hr_payslip.onchange_employee()
            hr_payslip.compute_sheet()
            hr_payslip.action_payslip_done()
            pmt_wizard = self.env['register.payment.wizard.journal'].with_context(active_model='hr.payslip',
                                                                           active_ids=hr_payslip.ids).create({
                'payment_date':hr_payslip.date,
                'employee_id':hr_payslip.employee_id.id,
                'payment_type': line.journal_id.id,
                'communication': hr_payslip.number,
                # 'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
                'amount': hr_payslip.total_amount_journal,
                'payslip_id':hr_payslip.id,
            })
            pmt_wizard.payment()
            # payment = self.env['account.payment'].create({
            #             'payment_type': 'outbound',
            #             'partner_id': line.hr_employee.address_home_id.id,
            #             'partner_type': 'supplier',
            #             'default_inbound_filter': 1,
            #             'move_journal_types': ('bank', 'cash'),
            #             'amount': hr_payslip.total_amount_journal,
            #             'payslip_id': hr_payslip.id,
            #             'payslip_visibility': True,
            #             'destination_account_id': self.env['account.account'].search(
            #                 [('name', '=', 'Wages Payable'), ('company_id', '=', self.env.user.company_id.id)]).id,
            #             'ref': self.number,
            #             'journal_id':line.journal_id.id,
            #
            #     })
            # print(payment,'payment')
            # payment.action_post()



        self.write({'state':'validate'})

    @api.onchange('branch_id')
    def onchange_branch_id(self):
        self.straw_expense_lines =False
        if self.branch_id:
            list = []
            for line in self.env['hr.employee'].search([('branch_id','=',self.branch_id.id)]):
                d = (0, 0, {
                    'hr_employee': line.id,
                })
                list.append(d)
            self.straw_expense_lines =list
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'branch.payslip') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('branch.payslip') or _('New')

        return super(BranchPayslip, self).create(vals)





class BranchWiseLines(models.Model):
    _name = 'branch.payslip.lines'

    # def default_branch_id(self):
    #     self.branch_payslip_id.branch_id

    branch_payslip_id = fields.Many2one('branch.payslip', 'Ref Name')
    hr_employee = fields.Many2one('hr.employee',string="Employee")
    journal_id = fields.Many2one('account.journal', string='Payment Journal', required=True, domain=[('type', 'in', ('bank', 'cash'))])


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    branch_id = fields.Many2one('company.branches', 'Branch Name')
    payslip_id = fields.Many2one('branch.payslip')

    @api.onchange('branch_id')
    def onchange_branch_id(self):
        if self.branch_id:
            return {'domain': {'employee_id': [('id', 'in', self.env['hr.employee'].search([('branch_id','=',self.branch_id.id)]).ids)]}}




class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    branch_id = fields.Many2one('company.branches', 'Branch Name')

class HrExpense(models.Model):
    _inherit = 'hr.expense'

    branch_id = fields.Many2one('company.branches', 'Branch Name')
