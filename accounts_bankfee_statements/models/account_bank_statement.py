from odoo import _, fields, models,api
from odoo.exceptions import UserError


from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.tools import float_is_zero
from odoo.tools import float_compare, float_round, float_repr
from odoo.tools.misc import formatLang, format_date
from odoo.exceptions import UserError, ValidationError

import time
import math
import base64
import re

class BankFeesStatement(models.Model):
    _name = "bank.fee.statement"
    _order = "id desc"


    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
    ], string='Status', copy=False, index=True, track_visibility='onchange', track_sequence=3,
        default='draft')
    create_date = fields.Date(string='Create Date', default=fields.Date.context_today, required=True)
    user_id = fields.Many2one('res.users', 'Users', index=True, ondelete='cascade', default=lambda self: self.env.user)
    # next_v_lines = fields.One2many('bank.fee.statement.line', 'bank_fee_id')
    journal_id = fields.Many2one('account.journal', string="Journal Name",domain=[('type', '=', 'bank')])
    fee_amount = fields.Float(string="Fee Amount")
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    note = fields.Text(string="Note")


    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            # if 'company_id' in vals:
            #     vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
            #         'bank.fee.statement') or _('New')
            # else:
                vals['name'] = self.env['ir.sequence'].next_by_code('bank.fee.statement') or _('New')
        return super(BankFeesStatement, self).create(vals)

    # def action_credit_statement(self):
    #     print('kdskf')
    #     self.write({'state':'confirm'})
    #
    #     vals = {
    #         'journal_id': self.journal_id.id ,
    #         'state': 'draft',
    #         'ref': self.note  or self.name,
    #         'company_id':self.company_id.id,
    #     }
    #     pay_id_list = []
    #     move_id = self.env['account.move'].create(vals)
    #     # partner_id = driver_id.id
    #     label = self.note
    #     bank_fee_config = self.env['account.reconcile.model'].search(
    #         [('name', '=', "Bank Fees"), ('company_id', '=', self.company_id.id)])
    #     lists= []
    #     if bank_fee_config:
    #         temp = (0, 0, {'quantity': 1,
    #                        'price_unit': self.fee_amount,
    #                        'name': 'test',
    #                        'account_id': self.journal_id.default_account_id.id,
    #                        'tax_ids': bank_fee_config.line_ids[0].tax_ids.ids,
    #                        })
    #         lists.append(temp)
    #     move_id.invoice_line_ids = lists
    #
    #     # if self.type_of_credit == False:
    #     temp = (0, 0, {
    #         'account_id':  self.journal_id.default_account_id.id,
    #         'name': label,
    #         'move_id': move_id.id,
    #         'date': self.create_date,
    #         # 'partner_id': driver_id.id,
    #         'debit': 0,
    #         'credit': self.fee_amount,
    #         'reconcile_model_id':self.env['account.reconcile.model'].search([('name','=',"Bank Fees"),('company_id','=',self.company_id.id)]).id
    #     })
    #     pay_id_list.append(temp)
    #     acc = self.env['account.account']
    #     debit_amount = self.fee_amount
    #     bank_fee_config = self.env['account.reconcile.model'].search([('name','=',"Bank Fees"),('company_id','=',self.company_id.id)])
    #     if bank_fee_config:
    #         if bank_fee_config.line_ids:
    #            acc = bank_fee_config.line_ids[0].account_id.id
    #            if bank_fee_config.line_ids[0].tax_ids:
    #                if bank_fee_config.line_ids.force_tax_included:
    #                    value = 100 + bank_fee_config.line_ids[0].tax_ids[0].amount
    #                    debit_amount = self.fee_amount * 100 / value
    #                else:
    #                    debit_amount = self.fee_amount
    #            else:
    #                debit_amount = self.fee_amount
    #     # else:
    #     #     debit_amount = self.fee_amount
    #
    #
    #     else:
    #         raise UserError(_('Please Createb Bank Fee reconciliation model under accounting setting'))
    #
    #     # acc = self.env['account.account'].sudo().search(
    #     #     [('name', '=', 'Bank Charges'),
    #     #      ('company_id', '=', self.company_id.id)])
    #     temp = (0, 0, {
    #         'account_id': acc,
    #         'name': label,
    #         'move_id': move_id.id,
    #         'date': self.create_date,
    #         # 'partner_id': driver_id.id,
    #         'debit': debit_amount,
    #         'credit': 0,
    #         # 'reconcile_model_id': self.env['account.reconcile.model'].search(
    #         #     [('name', '=', "Bank Fees"), ('company_id', '=', self.company_id.id)]).id
    #
    #     })
    #     pay_id_list.append(temp)
    #     if bank_fee_config:
    #         for tax in bank_fee_config.line_ids.tax_ids:
    #             debit_amounts = debit_amount
    #             if tax.children_tax_ids:
    #                for children in tax.children_tax_ids:
    #                       if bank_fee_config.line_ids.force_tax_included:
    #                           debit_amounts = debit_amount/ 100*children.amount
    #                           temp = (0, 0, {
    #                                 'account_id':children.invoice_repartition_line_ids.mapped('account_id').id,
    #                                 'name': label,
    #                                 'move_id': move_id.id,
    #                                 'date': self.create_date,
    #                                 # 'partner_id': driver_id.id,
    #                                 'debit': debit_amounts,
    #                                 'credit': 0,
    #                                 # 'reconcile_model_id': self.env['account.reconcile.model'].search(
    #                                 #     [('name', '=', "Bank Fees"), ('company_id', '=', self.company_id.id)]).id
    #                           })
    #                           pay_id_list.append(temp)
    #                       else:
    #                           debit_amounts = debit_amount / 100 * children.amount
    #                           temp = (0, 0, {
    #                               'account_id': children.invoice_repartition_line_ids.mapped('account_id').id,
    #                               'name': label,
    #                               'move_id': move_id.id,
    #                               'date': self.create_date,
    #                               # 'partner_id': driver_id.id,
    #                               'debit': debit_amounts,
    #                               'credit': 0,
    #                               # 'reconcile_model_id': self.env['account.reconcile.model'].search(
    #                               #     [('name', '=', "Bank Fees"), ('company_id', '=', self.company_id.id)]).id
    #                           })
    #                           pay_id_list.append(temp)
    #                           debit_amounts = debit_amount / 100 * children.amount
    #                           temp = (0, 0, {
    #                               'account_id': self.env['account.account'].search([('name','=','Reverse Charge Tax Receivable'),('company_id','=',self.company_id.id)]).id,
    #                               'name': label,
    #                               'move_id': move_id.id,
    #                               'date': self.create_date,
    #                               # 'partner_id': driver_id.id,
    #                               'debit': 0,
    #                               'credit': debit_amounts,
    #                               # 'reconcile_model_id': self.env['account.reconcile.model'].search(
    #                               #     [('name', '=', "Bank Fees"), ('company_id', '=', self.company_id.id)]).id
    #                           })
    #                           pay_id_list.append(temp)
    #
    #
    #     move_id.line_ids = pay_id_list
    #     move_id.sudo().action_post()
    #     mm = self.env['account.account'].sudo().search(
    #         [('name', '=', 'Bank Charges'),
    #          ('company_id', '=', self.company_id.id)])
    #     bank_stmt = self.env['account.bank.statement'].create({
    #         'journal_id': self.journal_id.id,
    #         'date': self.create_date,
    #         'line_ids': [
    #             (0, 0, {
    #                 'payment_ref': 'test',
    #                 # 'partner_id': se.id,
    #                 'amount': self.fee_amount,
    #                 'date': self.create_date,
    #                 # 'account_id':mm.id
    #             })
    #         ],
    #     })
    #
    #     # Reconcile the bank statement with the invoice.
    #     receivable_line = move_id.line_ids.filtered(
    #         lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
    #     bank_stmt.button_post()
    #     # counterpart_lines = move.mapped('line_ids').filtered(lambda line: line.account_internal_type in ('receivable', 'payable'))
    #
    #     bank_stmt.action_bank_reconcile_bank_statements()
    #     print('bank_stmt', bank_stmt)
    #     # bank_stmt.write({'state':'confirm'})
    #     #
    #     # mm = self.env['account.account'].sudo().search(
    #     #                 [('name', '=', 'Bank Charges'),
    #     #                  ('company_id', '=', self.company_id.id)])
    #     # bank_stmt.line_ids[0].reconcile([
    #     #     {'id': receivable_line.id},
    #     #     {'name': 'exchange difference', 'balance': -self.fee_amount, 'account_id':mm.id},
    #     # ])
    #     # # bank_stmt.reconcile([{'id': move_id.line_ids.id}])
    #
    #
    #
    #     # pay_id_lists = []
    #     # for k in move_id.line_ids:
    #     #     pay_id_lists.append(k.id)
    #     #
    #     # stmt = self.env['account.bank.statement']
    #     # if not stmt:
    #     #     journ = self.journal_id
    #     #     if self.env['account.bank.statement'].search(
    #     #             [('company_id', '=', journ.company_id.id), ('journal_id', '=', journ.id)]):
    #     #         bal = self.env['account.bank.statement'].search(
    #     #             [('company_id', '=', journ.company_id.id), ('journal_id', '=', journ.id)])[
    #     #             0].balance_end_real
    #     #     else:
    #     #         bal = 0
    #     #     stmt = self.env['account.bank.statement'].create({'name': self.note or self.name,
    #     #                                                       'balance_start': bal,
    #     #                                                       # 'journal_id': line.journal_id.id,
    #     #                                                       'journal_id': self.journal_id.id,
    #     #                                                       'balance_end_real': bal - self.fee_amount
    #     #
    #     #                                                       })
    #     #     payment_list = []
    #     #     product_line = (0, 0, {
    #     #         'date': self.create_date,
    #     #         'name': self.name,
    #     #         # 'partner_id': self.name,
    #     #         'payment_ref': self.note or self.name,
    #     #         'amount': -self.fee_amount,
    #     #         # 'move_id':move_id.id,
    #     #     })
    #     #
    #     #     payment_list.append(product_line)
    #     #
    #     # # move_id.action_cash_book()
    #     # if stmt:
    #     #     stmt.line_ids = payment_list
    #     #     # stmt.line_ids.mapped()
    #     #     move_id = stmt.line_ids.mapped('invoice_line_ids').mapped('move_id')
    #     #     # for each_m in move_id:
    #     #     #     each_m.unlink()
    #     #
    #     #     # stmt.move_line_ids = pay_id_list
    #     #     stmt.line_ids.invoice_line_ids = pay_id_lists
    #     #     stmt.write({'state': 'confirm'})
    #     #
    #     #


    # def action_credit_statement(self):
    #     bank_fee_config = self.env['account.reconcile.model'].search(
    #         [('name', '=', "Bank Fees"), ('company_id', '=', self.company_id.id)])
    #         # if bank_fee_config:
    #         #     if bank_fee_config.line_ids:
    #         #        acc = bank_fee_config.line_ids[0].account_id.id
    #         #        if bank_fee_config.line_ids[0].tax_ids
    #     list = []
    #     move = self.env['account.move'].create({
    #         # 'move_type': 'in_invoice',
    #         # 'partner_id': partner.id,
    #         'invoice_date': self.create_date,
    #         'date': self.create_date,
    #         'journal_id': self.journal_id.id,
    #         # 'currency_id': self.currency_usd_id,
    #         'invoice_line_ids': [
    #
    #         ],
    #     })
    #
    #     temp = (0, 0, {'quantity': 1,
    #                     'price_unit':self.fee_amount,
    #                     'name': 'test',
    #                    'account_id': self.journal_id.default_account_id.id,
    #                     'tax_ids':bank_fee_config.line_ids[0].tax_ids.ids,
    #                     })
    #     list.append(temp)
    #     move.invoice_line_ids = list
    #     move.action_post()
    #     print(move,'move')
    #
    #     # Create a bank statement of 40 EURO.
    #     mm = self.env['account.account'].sudo().search(
    #         [('name', '=', 'Bank Charges'),
    #          ('company_id', '=', self.company_id.id)])
    #     bank_stmt = self.env['account.bank.statement'].create({
    #         'journal_id': self.journal_id.id,
    #         'date':self.create_date,
    #         'line_ids': [
    #             (0, 0, {
    #                 'payment_ref': 'test',
    #                 # 'partner_id': se.id,
    #                 'amount': self.fee_amount,
    #                 'date':self.create_date,
    #                 # 'account_id':mm.id
    #             })
    #         ],
    #     })
    #
    #     # Reconcile the bank statement with the invoice.
    #     receivable_line = move.line_ids.filtered(
    #         lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
    #     bank_stmt.button_post()
    #     # counterpart_lines = move.mapped('line_ids').filtered(lambda line: line.account_internal_type in ('receivable', 'payable'))
    #
    #     bank_stmt.action_bank_reconcile_bank_statements()
    #     print('bank_stmt',bank_stmt)
    #     mm = self.env['account.account'].sudo().search(
    #                 [('name', '=', 'Bank Charges'),
    #                  ('company_id', '=', self.company_id.id)])
    #     # bank_stmt.line_ids[0].reconcile([
    #     #     {'id': receivable_line.id},
    #     #     {'name': 'exchange difference', 'balance': -self.fee_amount, 'account_id':mm.id},
    #     # ])
    #     # bank_stmt.reconcile([{'id': move.line_ids.id}])
    #     # bank_stmt.button_validate_or_action()
    #
    #     # self.assertRecordValues(bank_stmt.line_ids.line_ids, [
    #     #     {'debit': 40.0, 'credit': 0.0, 'amount_currency': 40.0, 'currency_id': self.currency_euro_id},
    #     #     {'debit': 0.0, 'credit': 7.3, 'amount_currency': -7.3, 'currency_id': self.currency_euro_id},
    #     #     {'debit': 0.0, 'credit': 32.7, 'amount_currency': -32.7, 'currency_id': self.currency_euro_id},
    #     # ])




    # def action_credit_statement(self):
    #     print('kdskf')
    #     self.write({'state':'confirm'})
    #     debit_amount = self.fee_amount
    #     bank_fee_config = self.env['account.reconcile.model'].search(
    #         [('name', '=', "Bank Fees"), ('company_id', '=', self.company_id.id)])
    #     if bank_fee_config:
    #         if bank_fee_config.line_ids:
    #             acc = bank_fee_config.line_ids[0].account_id.id
    #             if bank_fee_config.line_ids[0].tax_ids:
    #                 if bank_fee_config.line_ids.force_tax_included:
    #                     value = 100 + bank_fee_config.line_ids[0].tax_ids[0].amount
    #                     debit_amount = self.fee_amount * 100 / value
    #                 else:
    #                     debit_amount = self.fee_amount
    #             else:
    #                 debit_amount = self.fee_amount
    #     else:
    #         raise UserError(_('Please Createb Bank Fee reconciliation model under accounting setting'))
    #
    #     bank_stmt = self.env['account.bank.statement'].create({
    #         'journal_id': self.journal_id.id,
    #         'date': self.create_date,
    #         'bank_fee_enz':True,
    #         'line_ids': [
    #             (0, 0, {
    #                 'payment_ref': 'ENZAPPS MOUNIKA',
    #                 'partner_id':2,
    #                 'amount': self.fee_amount,
    #                 'date': self.create_date,
    #                 # 'account_id':mm.id
    #             })
    #         ],
    #     })
    #     print(bank_stmt,'bank_stmt')
    #     st_line = []
    #     for line in bank_stmt.line_ids:
    #         st_line.append(line.id)
    #
    #     # @api.model
    #     st_line_ids=st_line
    #     data=[
    #         {
    #             'partner_id': 40,
    #             'counterpart_aml_dicts': [],
    #             'payment_aml_ids': [],
    #             'new_aml_dicts':
    #                 [{'name': 'Bank Fees',
    #                   'debit': 0,
    #                   'credit': 254.24,
    #                   'analytic_tag_ids': [[6, None, []]],
    #                   'account_id': 59,
    #                   'tax_ids': [[6, None, [81]]],
    #                   'reconcile_model_id': 3},
    #                  {'name': 'trereyery',
    #                   'debit': 0,
    #                   'credit': 22.88,
    #                   'analytic_tag_ids': [[6, None, []]],
    #                   'account_id': 31,
    #                   'tax_tag_ids': [[6, None, [8]]],
    #                   # 'tax_repartition_line_id': 245
    #                   },
    #                  {'name': 'trereyery',
    #                   'debit': 0, 'credit': 22.88,
    #                   'analytic_tag_ids': [[6, None, []]],
    #                   'account_id': 32,
    #                   'tax_tag_ids': [[6, None, [10]]],
    #                   # 'tax_repartition_line_id': 247
    #                   }],
    #             'to_check': False}]
    #     self.env['account.reconciliation.widget'].process_bank_statement_line(st_line_ids, data)
    #
    #
    #     # Reconcile the bank statement with the invoice.
    #     move_id = bank_stmt.move_line_ids.mapped('move_id')
    #     # print('bank_stmt', bank_stmt)
    #     # statement = bank_stmt
    #     # statement_line = statement.line_ids
    #     # lists = []
    #     # statement.move_line_ids.mapped('move_id').button_draft()
    #     #
    #     # acc = self.env['account.account'].sudo().search(
    #     #             [('name', '=', 'Bank Charges'),
    #     #              ('company_id', '=', self.company_id.id)])
    #     # statement.move_line_ids.filtered(lambda a: a.account_id.name == 'Bank Suspense Account').account_id = acc
    #     #
    #     # pay_id_list = []
    #     # # move_id = self.env['account.move'].create(vals)
    #     # # # partner_id = driver_id.id
    #     # label = self.note
    #     # bank_fee_config = self.env['account.reconcile.model'].search(
    #     #     [('name', '=', "Bank Fees"), ('company_id', '=', self.company_id.id)])
    #     # lists = []
    #     # if bank_fee_config:
    #     #     temp = (0, 0, {'quantity': 1,
    #     #                    'price_unit': self.fee_amount,
    #     #                    'name': 'test',
    #     #                    'move_id':move_id.id,
    #     #                    'account_id': self.journal_id.default_account_id.id,
    #     #                    'tax_ids': bank_fee_config.line_ids[0].tax_ids.ids,
    #     #                    })
    #     #     lists.append(temp)
    #     # pay_id_list.append(temp)
    #     # acc = self.env['account.account']
    #     # debit_amount = self.fee_amount
    #     # bank_fee_config = self.env['account.reconcile.model'].search(
    #     #     [('name', '=', "Bank Fees"), ('company_id', '=', self.company_id.id)])
    #     # if bank_fee_config:
    #     #     if bank_fee_config.line_ids:
    #     #         acc = bank_fee_config.line_ids[0].account_id.id
    #     #         if bank_fee_config.line_ids[0].tax_ids:
    #     #             if bank_fee_config.line_ids.force_tax_included:
    #     #                 value = 100 + bank_fee_config.line_ids[0].tax_ids[0].amount
    #     #                 debit_amount = self.fee_amount * 100 / value
    #     #             else:
    #     #                 debit_amount = self.fee_amount
    #     #         else:
    #     #             debit_amount = self.fee_amount
    #     # else:
    #     #     raise UserError(_('Please Createb Bank Fee reconciliation model under accounting setting'))
    #     # temp = (0, 0, {
    #     #     'account_id': acc,
    #     #     'name': label,
    #     #     'move_id': move_id.id,
    #     #     'date': self.create_date,
    #     #     # 'partner_id': driver_id.id,
    #     #     'debit': debit_amount,
    #     #     'credit': 0,
    #     # })
    #     # pay_id_list.append(temp)
    #     # if bank_fee_config:
    #     #     for tax in bank_fee_config.line_ids.tax_ids:
    #     #         debit_amounts = debit_amount
    #     #         if tax.children_tax_ids:
    #     #             for children in tax.children_tax_ids:
    #     #                 if bank_fee_config.line_ids.force_tax_included:
    #     #                     debit_amounts = debit_amount / 100 * children.amount
    #     #                     temp = (0, 0, {
    #     #                         'account_id': children.invoice_repartition_line_ids.mapped('account_id').id,
    #     #                         'name': label,
    #     #                         'move_id': move_id.id,
    #     #                         'date': self.create_date,
    #     #                         # 'partner_id': driver_id.id,
    #     #                         'debit': debit_amounts,
    #     #                         'credit': 0,
    #     #                         # 'reconcile_model_id': self.env['account.reconcile.model'].search(
    #     #                         #     [('name', '=', "Bank Fees"), ('company_id', '=', self.company_id.id)]).id
    #     #                     })
    #     #                     pay_id_list.append(temp)
    #     #                 else:
    #     #                     debit_amounts = debit_amount / 100 * children.amount
    #     #                     temp = (0, 0, {
    #     #                         'account_id': children.invoice_repartition_line_ids.mapped('account_id').id,
    #     #                         'name': label,
    #     #                         'move_id': move_id.id,
    #     #                         'date': self.create_date,
    #     #                         # 'partner_id': driver_id.id,
    #     #                         'debit': debit_amounts,
    #     #                         'credit': 0,
    #     #                         # 'reconcile_model_id': self.env['account.reconcile.model'].search(
    #     #                         #     [('name', '=', "Bank Fees"), ('company_id', '=', self.company_id.id)]).id
    #     #                     })
    #     #                     pay_id_list.append(temp)
    #     #                     debit_amounts = debit_amount / 100 * children.amount
    #     #                     temp = (0, 0, {
    #     #                         'account_id': self.env['account.account'].search(
    #     #                             [('name', '=', 'Reverse Charge Tax Receivable'),
    #     #                              ('company_id', '=', self.company_id.id)]).id,
    #     #                         'name': label,
    #     #                         'move_id': move_id.id,
    #     #                         'date': self.create_date,
    #     #                         # 'partner_id': driver_id.id,
    #     #                         'debit': 0,
    #     #                         'credit': debit_amounts,
    #     #                         # 'reconcile_model_id': self.env['account.reconcile.model'].search(
    #     #                         #     [('name', '=', "Bank Fees"), ('company_id', '=', self.company_id.id)]).id
    #     #                     })
    #     #                     pay_id_list.append(temp)
    #     # statement.button_post()
    #     # statement.write({'state': 'confirm'})


    def action_credit_statement(self):
        print('kdskf')
        self.write({'state':'confirm'})

        bank_stmt = self.env['account.bank.statement'].create({
            'journal_id': self.journal_id.id,
            'date': self.create_date,
            'bank_fee_enz':True,
            'line_ids': [
                (0, 0, {
                    'payment_ref': self.note,
                    'partner_id':2,
                    'amount': -self.fee_amount,
                    'date': self.create_date,
                    # 'account_id':mm.id
                })
            ],
        })
        print(bank_stmt,'bank_stmt')
        st_line = []
        for line in bank_stmt.line_ids:
            st_line.append(line.id)

        # @api.model
        st_line_ids=st_line
        debit_amount = self.fee_amount
        bank_fee_config = self.env['account.reconcile.model'].search(
            [('name', '=', "Bank Fees"), ('company_id', '=', self.company_id.id)])
        if bank_fee_config:
            if bank_fee_config.line_ids:
                acc = bank_fee_config.line_ids[0].account_id.id
                if bank_fee_config.line_ids[0].tax_ids:
                    if bank_fee_config.line_ids.force_tax_included:
                        value = 100 + bank_fee_config.line_ids[0].tax_ids[0].amount
                        debit_amount = self.fee_amount * 100 / value
                    else:
                        debit_amount = self.fee_amount
                else:
                    debit_amount = self.fee_amount
        else:
            raise UserError(_('Please Createb Bank Fee reconciliation model under accounting setting'))
        if bank_fee_config:
            tax_list = []
            if bank_fee_config.line_ids.tax_ids:
                for tax in bank_fee_config.line_ids.tax_ids:
                    tax_list.append({'name': 'Bank Fees',
                     'debit': 0,
                     # 'credit': 254.24,
                     'credit': round(debit_amount),
                     'analytic_tag_ids': [[6, None, []]],
                     'account_id': self.env['account.account'].search([('name','=','Bank Charges'),('company_id','=',self.company_id.id)]).id,
                     'tax_ids': [[6, None, bank_fee_config.line_ids.tax_ids.ids]],
                     'reconcile_model_id': bank_fee_config.id})

                    debit_amounts = debit_amount
                    if tax.children_tax_ids:
                        for children in tax.children_tax_ids:
                            if children.tax_group_id.name == 'CGST':
                                if bank_fee_config.line_ids.force_tax_included:
                                    debit_amounts = debit_amount / 100 * children.amount
                                    tax_list.append({'name': self.note,
                                     'debit': 0,
                                     # 'credit': 22.88,
                                     'credit': round(debit_amounts),
                                     'analytic_tag_ids': [[6, None, []]],
                                     'account_id': self.env['account.account'].search([('name','=','CGST Payable'),('company_id','=',self.company_id.id)]).id,
                                     # 'tax_tag_ids': [[6, None, [8]]],
                                     # 'tax_repartition_line_id': 245
                                     })
                            if children.tax_group_id.name == 'SGST':
                                if bank_fee_config.line_ids.force_tax_included:
                                    debit_amounts = debit_amount / 100 * children.amount
                                    tax_list.append({'name':self.note,
                                     'debit': 0,
                                     # 'credit': 22.88,
                                     'credit': round(debit_amounts),
                                     'analytic_tag_ids': [[6, None, []]],
                                     'account_id': self.env['account.account'].search([('name','=','SGST Payable'),('company_id','=',self.company_id.id)]).id,
                                     # 'tax_tag_ids': [[6, None, [8]]],
                                     # 'tax_repartition_line_id': 245
                                     })

            else:

                tax_list.append({'name': 'Bank Fees',
                                 'debit': 0,
                                 # 'credit': 254.24,
                                 'credit': round(debit_amount),
                                 'analytic_tag_ids': [[6, None, []]],
                                 'account_id': self.env['account.account'].search(
                                     [('name', '=', 'Bank Charges'), ('company_id', '=', self.company_id.id)]).id,
                                 'tax_ids': [],
                                 'reconcile_model_id': self.env['account.reconcile.model'].search([('name','=','Bank Fees')]).id})

                # debit_amounts = debit_amount


                debit_amounts = debit_amount
            data = [{
                # 'partner_id': 40,
                'counterpart_aml_dicts': [],
                'payment_aml_ids': [],
                'new_aml_dicts': tax_list,
                'to_check': False}]
        # self.env['account.reconciliation.widget'].process_bank_statement_line(st_line_ids, data)
        # Reconcile the bank statement with the invoice.
        # move_id = bank_stmt.move_line_ids.mapped('move_id')
        bank_stmt.button_post()
        print(bank_stmt,'bank_stmt')
        # bank_stmt.button_validate_or_action()
        # bank_stmt.button_validate_or_action()
        bank_stmt.write({'state':'confirm'})

        # print('bank_stmt', bank_stmt)
        # statement = bank_stmt
        # statement_line = statement.line_ids
        # lists = []
        # statement.move_line_ids.mapped('move_id').button_draft()
        #
        # acc = self.env['account.account'].sudo().search(
        #             [('name', '=', 'Bank Charges'),
        #              ('company_id', '=', self.company_id.id)])
        # statement.move_line_ids.filtered(lambda a: a.account_id.name == 'Bank Suspense Account').account_id = acc
        #
        # pay_id_list = []
        # # move_id = self.env['account.move'].create(vals)
        # # # partner_id = driver_id.id
        # label = self.note
        # bank_fee_config = self.env['account.reconcile.model'].search(
        #     [('name', '=', "Bank Fees"), ('company_id', '=', self.company_id.id)])
        # lists = []
        # if bank_fee_config:
        #     temp = (0, 0, {'quantity': 1,
        #                    'price_unit': self.fee_amount,
        #                    'name': 'test',
        #                    'move_id':move_id.id,
        #                    'account_id': self.journal_id.default_account_id.id,
        #                    'tax_ids': bank_fee_config.line_ids[0].tax_ids.ids,
        #                    })
        #     lists.append(temp)
        # pay_id_list.append(temp)
        # acc = self.env['account.account']
        # debit_amount = self.fee_amount
        # bank_fee_config = self.env['account.reconcile.model'].search(
        #     [('name', '=', "Bank Fees"), ('company_id', '=', self.company_id.id)])
        # if bank_fee_config:
        #     if bank_fee_config.line_ids:
        #         acc = bank_fee_config.line_ids[0].account_id.id
        #         if bank_fee_config.line_ids[0].tax_ids:
        #             if bank_fee_config.line_ids.force_tax_included:
        #                 value = 100 + bank_fee_config.line_ids[0].tax_ids[0].amount
        #                 debit_amount = self.fee_amount * 100 / value
        #             else:
        #                 debit_amount = self.fee_amount
        #         else:
        #             debit_amount = self.fee_amount
        # else:
        #     raise UserError(_('Please Createb Bank Fee reconciliation model under accounting setting'))
        # temp = (0, 0, {
        #     'account_id': acc,
        #     'name': label,
        #     'move_id': move_id.id,
        #     'date': self.create_date,
        #     # 'partner_id': driver_id.id,
        #     'debit': debit_amount,
        #     'credit': 0,
        # })
        # pay_id_list.append(temp)
        # if bank_fee_config:
        #     for tax in bank_fee_config.line_ids.tax_ids:
        #         debit_amounts = debit_amount
        #         if tax.children_tax_ids:
        #             for children in tax.children_tax_ids:
        #                 if bank_fee_config.line_ids.force_tax_included:
        #                     debit_amounts = debit_amount / 100 * children.amount
        #                     temp = (0, 0, {
        #                         'account_id': children.invoice_repartition_line_ids.mapped('account_id').id,
        #                         'name': label,
        #                         'move_id': move_id.id,
        #                         'date': self.create_date,
        #                         # 'partner_id': driver_id.id,
        #                         'debit': debit_amounts,
        #                         'credit': 0,
        #                         # 'reconcile_model_id': self.env['account.reconcile.model'].search(
        #                         #     [('name', '=', "Bank Fees"), ('company_id', '=', self.company_id.id)]).id
        #                     })
        #                     pay_id_list.append(temp)
        #                 else:
        #                     debit_amounts = debit_amount / 100 * children.amount
        #                     temp = (0, 0, {
        #                         'account_id': children.invoice_repartition_line_ids.mapped('account_id').id,
        #                         'name': label,
        #                         'move_id': move_id.id,
        #                         'date': self.create_date,
        #                         # 'partner_id': driver_id.id,
        #                         'debit': debit_amounts,
        #                         'credit': 0,
        #                         # 'reconcile_model_id': self.env['account.reconcile.model'].search(
        #                         #     [('name', '=', "Bank Fees"), ('company_id', '=', self.company_id.id)]).id
        #                     })
        #                     pay_id_list.append(temp)
        #                     debit_amounts = debit_amount / 100 * children.amount
        #                     temp = (0, 0, {
        #                         'account_id': self.env['account.account'].search(
        #                             [('name', '=', 'Reverse Charge Tax Receivable'),
        #                              ('company_id', '=', self.company_id.id)]).id,
        #                         'name': label,
        #                         'move_id': move_id.id,
        #                         'date': self.create_date,
        #                         # 'partner_id': driver_id.id,
        #                         'debit': 0,
        #                         'credit': debit_amounts,
        #                         # 'reconcile_model_id': self.env['account.reconcile.model'].search(
        #                         #     [('name', '=', "Bank Fees"), ('company_id', '=', self.company_id.id)]).id
        #                     })
        #                     pay_id_list.append(temp)
        # statement.button_post()
        # statement.write({'state': 'confirm'})

class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    # @api.model_create_multi
    # def create(self, vals_list):
    #     # OVERRIDE
    #     counterpart_account_ids = []
    #
    #     for vals in vals_list:
    #         statement = self.env['account.bank.statement'].browse(vals['statement_id'])
    #         if statement.state != 'open' and self._context.get('check_move_validity', True):
    #             raise UserError(_("You can only create statement line in open bank statements."))
    #
    #         # Force the move_type to avoid inconsistency with residual 'default_move_type' inside the context.
    #         vals['move_type'] = 'entry'
    #
    #         journal = statement.journal_id
    #         # Ensure the journal is the same as the statement one.
    #         vals['journal_id'] = journal.id
    #         vals['currency_id'] = (journal.currency_id or journal.company_id.currency_id).id
    #         if 'date' not in vals:
    #             vals['date'] = statement.date
    #
    #         # Hack to force different account instead of the suspense account.
    #         counterpart_account_ids.append(vals.pop('counterpart_account_id', None))
    #
    #     st_lines = super().create(vals_list)
    #
    #     for i, st_line in enumerate(st_lines):
    #         counterpart_account_id = counterpart_account_ids[i]
    #
    #         to_write = {'statement_line_id': st_line.id}
    #         if 'line_ids' not in vals_list[i]:
    #             to_write['line_ids'] = [(0, 0, line_vals) for line_vals in st_line._prepare_move_line_default_vals(counterpart_account_id=counterpart_account_id)]
    #         if statement.bank_fee_enz:
    #            mounika =  self.testing_enzapps(statement)
    #            to_write['line_ids'] =mounika
    #         st_line.move_id.write(to_write)
    #
    #     return st_lines


    def testing_enzapps(self,statement):
        pay_id_list = []
        # move_id = self.env['account.move'].create(vals)
        # # partner_id = driver_id.id
        label = 'test'
        bank_fee_config = self.env['account.reconcile.model'].search(
            [('name', '=', "Bank Fees"), ('company_id', '=', statement.company_id.id)])
        lists = []
        # if bank_fee_config:
        #     temp = (0, 0, {'quantity': 1,
        #                    'price_unit': statement.fee_amount,
        #                    'name': 'test',
        #                    'account_id': statement.journal_id.default_account_id.id,
        #                    'tax_ids': bank_fee_config.line_ids[0].tax_ids.ids,
        #                    })
        #     lists.append(temp)
        # move_id.invoice_line_ids = lists

        # if self.type_of_credit == False:
        fee_amount = 1000
        acc = self.env['account.account']
        debit_amount = fee_amount
        bank_fee_config = self.env['account.reconcile.model'].search(
            [('name', '=', "Bank Fees"), ('company_id', '=', statement.company_id.id)])
        if bank_fee_config:
            if bank_fee_config.line_ids:
                acc = bank_fee_config.line_ids[0].account_id.id
                if bank_fee_config.line_ids[0].tax_ids:
                    if bank_fee_config.line_ids.force_tax_included:
                        value = 100 + bank_fee_config.line_ids[0].tax_ids[0].amount
                        debit_amount = fee_amount * 100 / value
                    else:
                        debit_amount = fee_amount
                else:
                    debit_amount = fee_amount
        else:
            raise UserError(_('Please Createb Bank Fee reconciliation model under accounting setting'))

        # acc = self.env['account.account'].sudo().search(
        #     [('name', '=', 'Bank Charges'),
        #      ('company_id', '=', self.company_id.id)])
        temp = (0, 0, {
            'account_id': acc,
            'name': label,
            'move_id': statement.move_line_ids.mapped('move_id').id,
            'date': statement.create_date,
            # 'partner_id': driver_id.id,
            'debit': debit_amount,
            'credit': 0,
            # 'reconcile_model_id': self.env['account.reconcile.model'].search(
            #     [('name', '=', "Bank Fees"), ('company_id', '=', self.company_id.id)]).id

        })
        pay_id_list.append(temp)
        if bank_fee_config:
            for tax in bank_fee_config.line_ids.tax_ids:
                debit_amounts = debit_amount
                if tax.children_tax_ids:
                    for children in tax.children_tax_ids:
                        if bank_fee_config.line_ids.force_tax_included:
                            debit_amounts = debit_amount / 100 * children.amount
                            temp = (0, 0, {
                                'account_id': children.invoice_repartition_line_ids.mapped('account_id').id,
                                'name': label,
                                'move_id': statement.move_line_ids.mapped('move_id').id,
                                'date': statement.create_date,
                                # 'partner_id': driver_id.id,
                                'debit': debit_amounts,
                                'credit': 0,
                                # 'reconcile_model_id': self.env['account.reconcile.model'].search(
                                #     [('name', '=', "Bank Fees"), ('company_id', '=', self.company_id.id)]).id
                            })
                            pay_id_list.append(temp)
                        else:
                            debit_amounts = debit_amount / 100 * children.amount
                            temp = (0, 0, {
                                'account_id': children.invoice_repartition_line_ids.mapped('account_id').id,
                                'name': label,
                                'move_id': statement.move_line_ids.mapped('move_id').id,
                                'date': statement.create_date,
                                # 'partner_id': driver_id.id,
                                'debit': debit_amounts,
                                'credit': 0,
                                # 'reconcile_model_id': self.env['account.reconcile.model'].search(
                                #     [('name', '=', "Bank Fees"), ('company_id', '=', self.company_id.id)]).id
                            })
                            pay_id_list.append(temp)
                            debit_amounts = debit_amount / 100 * children.amount
                            temp = (0, 0, {
                                'account_id': self.env['account.account'].search(
                                    [('name', '=', 'Reverse Charge Tax Receivable'),
                                     ('company_id', '=', statement.company_id.id)]).id,
                                'name': label,
                                'move_id': statement.move_line_ids.mapped('move_id').id,
                                'date': statement.create_date,
                                # 'partner_id': driver_id.id,
                                'debit': 0,
                                'credit': debit_amounts,
                                # 'reconcile_model_id': self.env['account.reconcile.model'].search(
                                #     [('name', '=', "Bank Fees"), ('company_id', '=', self.company_id.id)]).id
                            })
                            pay_id_list.append(temp)
        return pay_id_list


class AccountBankStatement(models.Model):
    _inherit = "account.bank.statement"

    bank_fee_enz = fields.Boolean(string="Bank Fee Enz")