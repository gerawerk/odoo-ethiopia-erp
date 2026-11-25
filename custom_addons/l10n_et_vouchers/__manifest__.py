# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Ethiopian Financial Vouchers (CPV, CRV, BPV, PCV)',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Standard Ethiopian corporate payment vouchers: CPV, CRV, BPV, PCV with automatic journal entries',
    'description': """
Ethiopian Financial Vouchers Suite
==================================
Implements mandatory Ethiopian corporate internal financial control vouchers
in accordance with AABE (Accounting & Auditing Board of Ethiopia) standards:

1. **CPV (Cash Payment Voucher / የጥሬ ገንዘብ ክፍያ ማዘዣ)**:
   - For all direct disbursements from main cash safe/cashier.
2. **CRV (Cash Receipt Voucher / የጥሬ ገንዘብ መቀበያ ሰነድ)**:
   - For all cash received by the cashier.
3. **BPV (Bank Payment Voucher / የባንክ ክፍያ ማዘዣ)**:
   - For payments via Cheque, CPO, or Electronic Bank Transfer (CBE, Awash, Telebirr, etc.).
4. **PCV (Petty Cash Voucher / የጥቃቅን ወጪ ማዘዣ)**:
   - For routine small business disbursements under petty cash fund.

Features:
- Dedicated sequential numbering for each voucher type (CPV, CRV, BPV, PCV).
- Automated double-entry Journal Entry (account.move) generation upon posting.
- Multi-line breakdown for multi-account expense allocation.
- Cheque, CPO, and bank transfer tracking.
- Bilingual Amharic and English amount-in-words representation.
- UI-configurable journals and account mappings.
    """,
    'author': 'Custom Ethiopian Localization Team',
    'depends': ['account', 'l10n_et_tax'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/et_voucher_views.xml',
        'views/et_voucher_menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
