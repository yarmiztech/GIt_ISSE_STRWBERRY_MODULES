from odoo import api, fields, models, tools, _


class ResUsers(models.Model):
    _inherit = "res.users"
    branch_id = fields.Many2one('company.branches')

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    _description = 'Purchase order'

    def default_branchs_boraque(self):
        if self.env.user.branch_id:
            return self.env.user.branch_id[0].id

    # branch_id = fields.Many2one('company.branches', string='Branch', domain="[('company_id','=',company_id)]",default=lambda self: self.env.user.branch_id[0].id)
    branch_id = fields.Many2one('company.branches', string='Branch', domain="[('company_id','=',company_id)]",default=default_branchs_boraque)

    
    # def action_view_invoice(self,moves):
    #     result = super(PurchaseOrder,self).action_view_invoice(moves)
    #     result['context'].update({'default_branch_id':self.branch_id.id})
    #     return result

class ResUsers(models.Model):
    _inherit = "res.users"

    branch_id = fields.Many2one('company.branches')
