from odoo import fields,models

class PreviousOccupation(models.Model):

    _name = "previous.occupation"
    _description = "Recruite Previous Occupation"
    _order = 'to_date desc'
    _rec_name = 'position'

    employee_id = fields.Many2one('hr.employee')
    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)
    position = fields.Char(string='Position', required=True)
    organization = fields.Char(string='Organization')
    ref_name = fields.Char(string='Reference Name')
    ref_position = fields.Char(string='Reference Position')
    ref_phone = fields.Char(string='Reference Phone')
    # active = fields.Boolean(string='Active', default=True)
    # applicant_id = fields.Many2one(
    #     'hr.applicant', 'Applicant Ref', ondelete='cascade')
    email = fields.Char('Email')