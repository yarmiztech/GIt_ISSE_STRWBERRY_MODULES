# -*- coding: utf-8 -*-
{
    'name': "Enzapps HR",
    'author':
        'ENZAPPS',
    'summary': """
This module is for Advanced HR Features.
""",

    'description': """
        This module is for Advanced HR Features.
    """,
    'website': "",
    'category': 'base',
    'version': '12.0',
    'depends': ['base', 'account', 'contacts', 'account', 'hr', 'om_hr_payroll', 'hr_holidays', 'hr_recruitment','payslip_payment_journal',
                'ohrms_loan','bonu_generation'],
    "images": ['static/description/icon.png'],
    'data': [
        'security/ir.model.access.csv',
        'reports/employee_detail.xml',
        'reports/employee_detail_view.xml',
        'data/alert_data.xml',
        'views/experience_certificate.xml',
        'views/hr_employee_inherit.xml',
        'views/offer_letter.xml',
        'views/alert.xml',
        'views/warning_form.xml',
        'views/emp_complete_report.xml',
        'views/loan_change.xml',
        'views/salary_payment.xml',
        'views/leave_form.xml',

    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
}
