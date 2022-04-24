# -*- coding: utf-8 -*-
{
    'name': "Bonus Creation",
    'author':
        'ENZAPPS',
    'summary': """
This module is for Creation Of Bonus Every Thursday.
""",

    'description': """
        This module is for Creation Of Bonus Every Thursday.
    """,
    'website': "",
    'category': 'base',
    'version': '12.0',
    'depends': ['base','contacts','account','hr','hr_contract'],
    "images": ['static/description/icon.png'],
    'data': [
        'security/ir.model.access.csv',
        'data/bonus_creation.xml',
        'reports/bonus_report_view.xml',
        'reports/bonus_report.xml',
        'views/bonuc_form.xml',
        'views/bonuc_rec.xml',
        'views/bonus_history.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
}
