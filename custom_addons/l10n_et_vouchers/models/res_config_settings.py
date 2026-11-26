# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    voucher_approval_threshold = fields.Monetary(
        related='company_id.voucher_approval_threshold',
        readonly=False,
    )
    voucher_require_checker = fields.Boolean(
        related='company_id.voucher_require_checker',
        readonly=False,
    )
