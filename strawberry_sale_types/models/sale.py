from odoo import fields,models,api
from odoo.tests.common import Form
from datetime import datetime

class SaleOrder(models.Model):
    _inherit = "sale.order"


    purchase_type_cash = fields.Selection(string='Cash/Credit', selection=[('cash', 'Cash Payment'),('bank', 'Bank Payment'), ('credit', 'Credit Payment')])
    branch_id = fields.Many2one('company.branches', 'Branch Name')
    bank_journal_id = fields.Many2one('account.journal',string='Select Bank',domain=[('type', '=', 'bank')])
    straw_quot_date = fields.Date(string="Straw Date")

    def _action_confirm(self):
        super(SaleOrder, self)._action_confirm()
        self.date_order = str(self.straw_quot_date) + ' 00:00:00'
        self.create_date = self.straw_quot_date
        invoice_ids = self._create_invoices()
        for i in invoice_ids:
            # account_move = self.env['account.move']
            # invoice_id = account_move.search([('id', '=', i.id)])
            # stock_ids = invoice_id.action_post()
            for pickings in self.picking_ids:
                pickings.action_assign()
                m = pickings.button_validate()
                print(m, "m")
                Form(self.env['stock.immediate.transfer'].with_context(m['context'])).save().process()
            for inv in i:
                inv.invoice_date = self.straw_quot_date
                inv.date = self.straw_quot_date
                inv.l10n_sa_delivery_date = self.straw_quot_date
                inv.invoice_date_due = self.straw_quot_date
                if inv.state != 'posted':
                    action_post_id = inv.action_post()
                inv.invoice_date = self.straw_quot_date
                if self.purchase_type_cash == 'cash':
                    pmt_wizard = self.env['account.payment.register'].with_context(active_model='account.move',
                                                                                   active_ids=inv.ids).create({
                        'payment_date': inv.invoice_date,
                        'journal_id': self.env['account.journal'].search(
                            [('name', '=', 'Cash'), ('company_id', '=', inv.company_id.id)]).id,
                        'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
                        'amount': inv.amount_total,
                    })
                    pmt_wizard._create_payments()
                if self.purchase_type_cash == 'bank':
                    pmt_wizard = self.env['account.payment.register'].with_context(active_model='account.move',
                                                                                   active_ids=inv.ids).create({
                        'payment_date': inv.invoice_date,
                        'journal_id': self.bank_journal_id.id,
                        'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
                        'amount': inv.amount_total,
                    })
                    pmt_wizard._create_payments()






