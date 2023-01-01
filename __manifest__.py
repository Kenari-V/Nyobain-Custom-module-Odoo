# -*- coding: utf-8 -*-
{
    'name': 'Buku Tamu',
    'version': '1.0.0',
    'category': 'Hospital',
    'summary': 'Hospital Management System',
    'description': """Hospital Management System""",
    'depends': ['base'],
    'data': [
        "security/ir.model.access.csv",
        "data/sequence.xml",
        # "data/mail.xml",
        "views/pengunjung_view.xml",
        "views/karyawan.xml",
        "views/ruangan.xml",
        # "views/qrcode.xml"
        "reports/report.xml"
        
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'assets': {},
}
