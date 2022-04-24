# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64

from odoo import fields, api, models
from datetime import datetime, date



class PosSession(models.Model):
    _inherit = 'pos.session'

    def action_pos_session_validate(self):
        rec = super(PosSession, self).action_pos_session_validate()
        print('fgfdgfdhfdh')
        for bank in self.payment_method_ids.filtered(lambda a:a.name != 'Cash'):
            journ = self.env['account.journal'].search([('name', '=',bank.display_name)])
            # bal = sum(self.env['account.move.line'].search([('journal_id', '=', line.debited_account.id)]).mapped(
            #     'debit'))
            if self.env['account.bank.statement'].search([]):
                if self.env['account.bank.statement'].search(
                        [('company_id', '=', journ.company_id.id), ('journal_id', '=', journ.id)]):
                    bal = self.env['account.bank.statement'].search(
                        [('company_id', '=', journ.company_id.id), ('journal_id', '=', journ.id)])[
                        0].balance_end_real
                else:
                    bal = 0
            else:
                credit = sum(self.env['account.move.line'].search([('account_id', '=', journ.payment_credit_account_id.id)]).mapped(
                    'debit'))
                debit = sum(self.env['account.move.line'].search(
                    [('account_id', '=', journ.payment_debit_account_id.id)]).mapped(
                    'debit'))
                bal = debit-credit
            bank_move_line = self.move_id.line_ids.filtered(lambda a: a.name == self.name + ' - ' + bank.display_name)
            stmt = self.env['account.bank.statement'].create({'name': journ.company_id.partner_id.name,
                                                              'balance_start': bal,
                                                              'journal_id': journ.id,
                                                              'balance_end_real': bal + bank_move_line.debit

                                                              })
            payment_list = []
            product_line = (0, 0, {
                'date': datetime.today().date(),
                'name': self.name,
                'partner_id': journ.company_id.partner_id.id,
                'payment_ref': self.name,
                'amount':bank_move_line.debit
            })
            payment_list.append(product_line)
            if stmt:
                stmt.line_ids = payment_list
                # self.move_id.write({'state':'posted'})
                # stmt.button_post()
                # else:
                # statement = self.cash_register_id
                # if not self.config_id.cash_control:
                stmt.button_post()
                # stmt.write({'balance_end_real': stmt.balance_end})
                # stmt.button_validate()
            # self.write({'state': 'closed'})




        return rec

    def action_pos_session_closing_control(self):
        rec = super(PosSession, self).action_pos_session_closing_control()
        for bank in self.payment_method_ids.filtered(lambda a: a.name != 'Cash'):
            journ = self.env['account.journal'].search([('name', '=', bank.display_name)])
            if self.env['account.bank.statement'].search([]):
                if self.env['account.bank.statement'].search(
                        [('company_id', '=', journ.company_id.id), ('journal_id', '=', journ.id)]):
                    bal = self.env['account.bank.statement'].search(
                        [('company_id', '=', journ.company_id.id), ('journal_id', '=', journ.id)])[
                        0].balance_end_real
                else:
                    bal = 0
            else:
                credit = sum(self.env['account.move.line'].search(
                    [('account_id', '=', journ.payment_credit_account_id.id)]).mapped(
                    'debit'))
                debit = sum(self.env['account.move.line'].search(
                    [('account_id', '=', journ.payment_debit_account_id.id)]).mapped(
                    'debit'))
                bal = debit - credit
            bank_move_line = self.move_id.line_ids.filtered(lambda a: a.name == self.name + ' - ' + bank.display_name)
            stmt = self.env['account.bank.statement'].create({'name': journ.company_id.partner_id.name,
                                                              'balance_start': bal,
                                                              'journal_id': journ.id,
                                                              'balance_end_real': bal + bank_move_line.debit

                                                              })
            payment_list = []
            product_line = (0, 0, {
                'date':  datetime.today().date(),
                'name': self.name,
                'partner_id': journ.company_id.partner_id.id,
                'payment_ref': self.name,
                'amount': bank_move_line.debit
            })
            payment_list.append(product_line)
            if stmt:
                stmt.line_ids = payment_list
                stmt.button_post()
                stmt.move_line_ids = False
                stmt.write({'state': 'confirm'})

        return

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.constrains('name', 'journal_id', 'state')
    def _check_unique_sequence_number(self):
        moves = self.filtered(lambda move: move.state == 'posted')
        if not moves:
            return

        self.flush(['name', 'journal_id', 'move_type', 'state'])

        # /!\ Computed stored fields are not yet inside the database.
        self._cr.execute('''
            SELECT move2.id, move2.name
            FROM account_move move
            INNER JOIN account_move move2 ON
                move2.name = move.name
                AND move2.journal_id = move.journal_id
                AND move2.move_type = move.move_type
                AND move2.id != move.id
            WHERE move.id IN %s AND move2.state = 'posted'
        ''', [tuple(moves.ids)])
        res = self._cr.fetchall()
        # if res:
        #     raise ValidationError(_('Posted journal entry must have an unique sequence number per company.\n'
        #                             'Problematic numbers: %s\n') % ', '.join(r[1] for r in res))

#
# class ClosingBalanceConfirm(models.TransientModel):
#     _inherit = 'closing.balance.confirm.wizard'
#     # _description = 'This wizard is used to display a warning message if the manager wants to close a session with a too high difference between real and expected closing balance'
#
#     def confirm_closing_balance(self):
#         # current_session =  self.env['pos.session'].browse(self._context['session_id'])
#         # return current_session._validate_session()
#         rec = super(ClosingBalanceConfirm, self).confirm_closing_balance()
#         print(rec)



