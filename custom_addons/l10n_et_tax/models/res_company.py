# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    et_tin_number = fields.Char(
        string='Company Ethiopian TIN',
        size=10,
        help='10-digit Tax Identification Number of the company',
    )
    et_vat_reg_number = fields.Char(
        string='Company VAT Reg. No.',
        help='Company official VAT registration number issued by MOR',
    )
    et_sub_city = fields.Char(
        string='Company Sub-City (ክፍለ ከተማ)',
    )
    et_woreda = fields.Char(
        string='Company Woreda (ወረዳ)',
    )
    et_house_number = fields.Char(
        string='Company House No. (የቤት ቁጥር)',
    )
    et_wht_enabled = fields.Boolean(
        string='Enable Withholding Tax (WHT)',
        default=True,
        help='Automatically calculate and withhold tax on qualifying vendor bills',
    )
    et_wht_goods_threshold = fields.Monetary(
        string='WHT Goods Threshold',
        default=10000.0,
        currency_field='currency_id',
        help='Minimum bill amount for supply of goods to trigger 2% Withholding Tax (Default: 10,000 ETB)',
    )
    et_wht_services_threshold = fields.Monetary(
        string='WHT Services Threshold',
        default=3000.0,
        currency_field='currency_id',
        help='Minimum bill amount for supply of services to trigger 2% Withholding Tax (Default: 3,000 ETB)',
    )
    et_wht_rate = fields.Float(
        string='Default WHT Rate (%)',
        default=2.0,
        digits=(5, 2),
        help='Withholding tax percentage to deduct (Default: 2.0%)',
    )
    et_wht_tax_id = fields.Many2one(
        'account.tax',
        string='Purchase WHT Tax Record',
        domain="[('type_tax_use', '=', 'purchase')]",
        help='Tax record applied when deducting Withholding Tax on purchase bills',
    )
    et_tot_goods_tax_id = fields.Many2one(
        'account.tax',
        string='Turnover Tax (Goods - 2%)',
        domain="[('type_tax_use', '=', 'sale')]",
        help='Default Turnover Tax for supply of goods by non-VAT registered businesses',
    )
    et_tot_services_tax_id = fields.Many2one(
        'account.tax',
        string='Turnover Tax (Services - 10%)',
        domain="[('type_tax_use', '=', 'sale')]",
        help='Default Turnover Tax for supply of services by non-VAT registered businesses',
    )
