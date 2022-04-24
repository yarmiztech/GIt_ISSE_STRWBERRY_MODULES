# -*- coding: utf-8 -*-
{
    'name': "Expenses Report Monthly",
    'author':
        'ENZAPPS',
    'summary': """
This module is for Monthly Expenses Report
""",

    'description': """
        This module is for Monthly Expenses Report.
    """,
    'website': "",
    'category': 'base',
    'version': '14.0',
    'depends': ['base', 'account','hr_expense','hr'],
    'data': [
        'security/ir.model.access.csv',
        'data/zone.xml',
        'views/expenses_report.xml',
        'report/collection.xml',
        'report/ledger_without.xml',
        'report/ledger_vat.xml',
        'report/ledger.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
}
