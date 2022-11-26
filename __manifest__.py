# -*- coding: utf-8 -*-
{
    'name': "booking_order_ahmadyd_odoo14",

    'summary': """
        Test Booking Order Odoo14""",

    'description': """
        Test Booking Order Odoo14
    """,

    'author': "Ahmad Yulian Dinata",
    'website': "https://www.linkedin.com/in/ahmaddyd/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',
    'application':True,

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        'views/cancel_order_view.xml',
        'security/ir.model.access.csv',
        'views/work_order_view.xml',
        'views/booking_order_view.xml',
        'views/service_team_view.xml',
        'views/menu.xml',
        'report/report_wo.xml',
        'report/report.xml',
        'data/data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}