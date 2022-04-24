# -*- coding: utf-8 -*-
{
    'name': "Payslip Payment Journal",
    'author':
        'Enzapps',
    'summary': """
    This is a module is for passing journal entry while payment of payslip.
""",

    'description': """
        This is a module is for passing journal entry while payment of payslip.
    """,
    'website': "www.enzapps.com",
    'category': 'base',
    'version': '12.0',
    'depends': ['base','om_hr_payroll'],
    "images": [],
    'data': [
        'security/ir.model.access.csv',
        'wizard/register_payment_wizard.xml',
        'views/hr_payslip_inherit.xml',
        # 'views/inherit_employee.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
}
