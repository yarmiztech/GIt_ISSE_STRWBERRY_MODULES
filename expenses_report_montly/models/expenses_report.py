from odoo import models, fields, api
from datetime import datetime, date
from uuid import uuid4

class ExpensesReportMontly(models.Model):
    _name = 'expenses.report.montly'
    _rec_name = 'date'
    _order = "id desc"

    from_date = fields.Date()
    to_date = fields.Date()
    expense_type = fields.Selection([
        ("without", "Without VAT"),
        ("with", "With VAT")
    ],string="Expense By")
    date = fields.Date(default=datetime.now().date())
    invoice_lines = fields.One2many('expenses.montly.lines', 'report_id')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id)


    @api.onchange('form_date', 'to_date','company_id','expense_type')
    def compute_invoices(self):
        if self.expense_type == 'without':
            invoices = self.env['hr.expense'].sudo().search(
                [('date', '<=', self.to_date), ('date', '>=', self.from_date),('tax_ids', '=',False),
                ])
        elif self.expense_type == 'with':
            invoices = self.env['hr.expense'].sudo().search(
                [('date', '<=', self.to_date), ('date', '>=', self.from_date), ('tax_ids', '!=', False),
                 ])
        else:
            invoices = self.env['hr.expense'].sudo().search(
                        [('date', '<=', self.to_date), ('date', '>=', self.from_date),
                        ])

        invoice_list = []
        vat_amount = 0
        for line in invoices:
            price = line.quantity * line.unit_amount
            if line.tax_ids:
                vat_amount = price*0.15
            else:
                vat_amount = 0.0
            invoice_line = (0, 0, {
                'hr_expense':line.id,
                # 'hr_expense_sheet':line.id,
                'employee_id':line.employee_id.id,
                'name':line.name,
                'product_id':line.product_id.id,
                'date':line.date,
                'tax_ids':line.tax_ids.id,
                'state':line.state,
                'payment_mode':line.payment_mode,
                'tax_excluded':price,
                'tax_amount':vat_amount,
                'total_amount':line.total_amount,
                })
            invoice_list.append(invoice_line)
        self.invoice_lines = None
        self.invoice_lines = invoice_list


class ExpensesMontlyLines(models.Model):
    _name = 'expenses.montly.lines'

    report_id = fields.Many2one('expenses.report.montly')
    hr_expense = fields.Many2one('hr.expense')
    date = fields.Date(string="Date")
    hr_expense_sheet = fields.Many2one('hr.expense.sheet')
    name = fields.Char('Description')
    employee_id = fields.Many2one('hr.employee')
    product_id = fields.Many2one('product.product',string="Product")
    payment_mode = fields.Selection([
        ("own_account", "Employee (to reimburse)"),
        ("company_account", "Company")
    ],string="Paid By")
    state = fields.Selection([
        ('draft', 'To Submit'),
        ('reported', 'Submitted'),
        ('approved', 'Approved'),
        ('done', 'Paid'),
        ('refused', 'Refused')
    ], string='Status', copy=False, index=True, store=True,
        help="Status of the expense.")
    tax_ids = fields.Many2one('account.tax')
    tax_excluded = fields.Float(string="Without VAT")
    tax_amount = fields.Float(string="VAT Amount")
    total_amount = fields.Float(string="Total Amount")


class Expense(models.Model):
    _inherit = "hr.expense"

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            if self.product_id.taxes_id:
                self.tax_ids = self.product_id.taxes_id

