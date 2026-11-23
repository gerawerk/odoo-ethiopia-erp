# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Ethiopian Tax & Accounting Localization',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Ethiopian 10-digit TIN validation, 15% VAT, 2%/10% TOT, and configurable WHT settings',
    'description': """
Ethiopian Tax & Accounting Localization (Days 1 & 2)
====================================================
- Enforces strict 10-digit Ethiopian TIN validation on customers and vendors.
- Standard Ethiopian Taxes:
  * VAT 15% (Sales & Purchases)
  * VAT 0% Export (Zero-Rated)
  * VAT Exempt
  * Turnover Tax (TOT) 2% on Goods
  * Turnover Tax (TOT) 10% on Services
  * Withholding Tax (WHT) 2%
- Configurable settings in Accounting Settings (Thresholds, Rates, and Default Tax records).
    """,
    'author': 'Custom Ethiopian Localization Team',
    'depends': ['account', 'l10n_et'],
    'data': [
        'data/account_tax_group_data.xml',
        'data/account_tax_data.xml',
        'views/res_partner_views.xml',
        'views/account_tax_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
