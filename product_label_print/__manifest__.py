# -*- coding: utf-8 -*-

{
    'name': 'Product Label Print',
    'version': '8.0',
    'website': 'https://www.odoo.com',
    'category': 'Stock',
    'summary': 'Product Label Print',
    'author': 'Kiran Kantesariya, Ahmet Altinisik',
    'description': """
     """,
    'depends': [
        'product', 'stock'
    ],
    'data': [
        'wizard/print_pack_barcode_wiz_view.xml',
        'views/product_view.xml',
        'views/printer.xml',
        'report/label_reports.xml',
        'report/reports.xml',
    ],
    'installable' : True,
    'auto_install' : False,
}
