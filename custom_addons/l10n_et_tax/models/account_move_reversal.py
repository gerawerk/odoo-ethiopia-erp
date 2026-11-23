# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields

class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'

    et_credit_reason = fields.Selection([
        ('goods_return', 'Goods Returned (የተመለሱ እቃዎች)'),
        ('price_correction', 'Price / Calculation Error (የዋጋ ወይም የስሌት ስህተት ማስተካከያ)'),
        ('post_sale_discount', 'Post-Sale Discount / Rebate (ከሽያጭ በኋላ የተሰጠ ቅናሽ)'),
        ('cancellation', 'Full Cancellation of Transaction (የግብይት መሰረዝ)'),
        ('other', 'Other Legal Reason (ሌላ ህጋዊ ምክንያት)'),
    ], string='MOR Legal Reason (የማስተካከያ ምክንያት)', default='goods_return',
       help='Mandatory reason for issuing credit note under Ethiopian VAT Proclamation No. 285/2002 Article 24')

    def _prepare_default_reversal(self, move):
        res = super()._prepare_default_reversal(move)
        if self.et_credit_reason:
            res['et_credit_reason'] = self.et_credit_reason
        res['et_original_invoice_id'] = move.id
        return res
