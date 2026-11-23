# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields

class AccountTax(models.Model):
    _inherit = 'account.tax'

    is_wht_tax = fields.Boolean(
        string='Is Withholding Tax (WHT)',
        default=False,
        help='Check if this tax is an Ethiopian Withholding Tax (WHT)',
    )
    is_tot_tax = fields.Boolean(
        string='Is Turnover Tax (TOT)',
        default=False,
        help='Check if this tax is an Ethiopian Turnover Tax (TOT)',
    )
