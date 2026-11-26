# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    voucher_approval_threshold = fields.Monetary(
        string='Executive Approval Threshold',
        default=50000.0,
        currency_field='currency_id',
        help='Vouchers exceeding this amount require Executive / Finance Director approval',
    )
    voucher_require_checker = fields.Boolean(
        string='Enforce Checker Stage',
        default=True,
        help='Enforces two-tier verification: Checker must verify before Approver authorizes',
    )
