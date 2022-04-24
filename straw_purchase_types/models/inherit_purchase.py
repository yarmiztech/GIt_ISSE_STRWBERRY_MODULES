from odoo import fields,models,api
from odoo.tests.common import Form
from datetime import datetime

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    purchase_type_cash = fields.Selection(string='Cash/Credit', selection=[('cash', 'Cash Payment'),('bank', 'Bank Payment'), ('credit', 'Credit Payment')])
    branch_id = fields.Many2one('company.branches', 'Branch Name')
    bank_journal_id = fields.Many2one('account.journal',string='Select Bank',domain=[('type', '=', 'bank')])
    straw_quot_date = fields.Date(string="Straw Date")

    def button_confirm(self):
        super(PurchaseOrder, self).button_confirm()
        self.date_order = str(self.straw_quot_date) + ' 00:00:00'
        self.date_approve = str(self.straw_quot_date) + ' 00:00:00'
        self.date_planned = str(self.straw_quot_date) + ' 00:00:00'
        self.effective_date = str(self.straw_quot_date) + ' 00:00:00'
        if self.purchase_type_cash:
            # self.purchase_order_id = self.id
            receive_prod_id =self.action_view_picking()
            stock_picking = self.env['stock.picking'].search([('purchase_id', '=', self.id)])
            validate = stock_picking.button_validate()
            Form(self.env['stock.immediate.transfer'].with_context(validate['context'])).save().process()
            create_bill_id = self.action_create_invoice()
            # invoices_list = self.env['account.move'].search([('purchase_id','=',self.id)])
            for inv in self.invoice_ids:
                for inv_line in inv.invoice_line_ids:
                    if not inv_line.tax_ids:
                        inv_line.account_id = self.env['account.account'].search([('name','=','Purchase(without Vat)')])
                inv.invoice_date = datetime.now().date()
                inv.invoice_date = self.straw_quot_date
                inv.date = self.straw_quot_date
                inv.invoice_date_due = self.straw_quot_date
                # inv.l10n_in_gst_treatment = inv.partner_id.l10n_in_gst_treatment
                if inv.state != 'posted':
                    action_post_id = inv.action_post()
                if self.purchase_type_cash == 'cash':
                    pmt_wizard = self.env['account.payment.register'].with_context(active_model='account.move',
                                                                                   active_ids=inv.ids).create({
                        'payment_date':inv.invoice_date,
                        'journal_id': self.env['account.journal'].search(
                            [('name', '=', 'Cash'), ('company_id', '=', inv.company_id.id)]).id,
                        'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
                        'amount': inv.amount_total,
                    })
                    pmt_wizard._create_payments()
                if self.purchase_type_cash == 'bank':
                    pmt_wizard = self.env['account.payment.register'].with_context(active_model='account.move',
                                                                                   active_ids=inv.ids).create({
                        'payment_date':inv.invoice_date,
                        'journal_id': self.bank_journal_id.id,
                        'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
                        'amount': inv.amount_total,
                    })
                    pmt_wizard._create_payments()





