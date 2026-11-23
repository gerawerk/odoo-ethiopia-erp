# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Ethiopian Tax & Accounting Localization',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Ethiopian 10-digit TIN, 15% VAT, 2%/10% TOT, automated 2% WHT, and Credit Note compliance',
    'description': """
Ethiopian Tax & Accounting Localization
========================================
- Enforces strict 10-digit Ethiopian TIN validation on customers and vendors.
- Ethiopian VAT & Turnover Taxes (VAT 15%, 0%, Exempt, TOT 2%, TOT 10%).
- Automated 2% Withholding Tax deduction on vendor bills (Goods >= 10k ETB, Services >= 3k ETB).
- Ethiopian Credit Note & Refund Compliance (MOR Proclamation No. 285/2002 Article 24):
  * Mandatory legal reason selector (Goods Return, Price Error, Post-Sale Discount, Cancellation).
  * Direct linking to the original Tax Invoice number and date.
  * Reversal wizard integration.
- Ethiopian Address Format (Sub-City, Woreda, House No).
- Fiscal Cash Register (FCR / ESRM) tracking fields.
    """,
    'author': 'Custom Ethiopian Localization Team',
    'depends': ['account', 'l10n_et'],
    'data': [
        'data/account_tax_group_data.xml',
        'data/account_tax_data.xml',
        'views/res_partner_views.xml',
        'views/account_tax_views.xml',
        'views/res_config_settings_views.xml',
        'views/account_move_views.xml',
        'views/account_move_reversal_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
