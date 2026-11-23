# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    tin_number = fields.Char(
        string='Ethiopian TIN',
        size=10,
        help='10-digit Tax Identification Number issued by Ministry of Revenues (MOR)',
        tracking=True,
    )
    is_withholding_agent = fields.Boolean(
        string='Withholding Agent',
        default=False,
        help='Check if this partner is an authorized withholding tax agent',
    )
    is_vat_registered = fields.Boolean(
        string='VAT Registered',
        default=True,
        help='Uncheck if the partner is subject to Turnover Tax (TOT) instead of VAT',
    )

    @api.constrains('tin_number')
    def _check_tin_number(self):
        for partner in self:
            if partner.tin_number:
                tin = partner.tin_number.strip()
                # Ethiopian TIN has invariant size of 10 numeric digits
                if len(tin) != 10 or not tin.isdigit():
                    raise ValidationError(_(
                        "Invalid Ethiopian TIN '%(tin)s' for partner '%(name)s'!\n"
                        "An Ethiopian Tax Identification Number (TIN) must be strictly 10 numeric digits.",
                        tin=partner.tin_number,
                        name=partner.name,
                    ))
