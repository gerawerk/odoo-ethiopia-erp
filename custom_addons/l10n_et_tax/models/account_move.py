# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from ..tools.amount_to_text_am import amount_to_amharic

class AccountMove(models.Model):
    _inherit = 'account.move'

    # Related Ethiopian Partner Compliance Fields
    partner_tin_number = fields.Char(
        string='Partner TIN',
        related='partner_id.tin_number',
        readonly=True,
        help='10-digit Tax Identification Number of the partner',
    )
    partner_vat_reg_number = fields.Char(
        string='Partner VAT Reg. No.',
        related='partner_id.vat_reg_number',
        readonly=True,
        help='VAT Registration Number of the partner',
    )
    partner_sub_city = fields.Char(
        string='Partner Sub-City',
        related='partner_id.sub_city',
        readonly=True,
    )
    partner_woreda = fields.Char(
        string='Partner Woreda',
        related='partner_id.woreda',
        readonly=True,
    )
    partner_house_number = fields.Char(
        string='Partner House No.',
        related='partner_id.house_number',
        readonly=True,
    )

    # Ethiopian Credit Note (MOR Article 24) Compliance Fields
    is_credit_note = fields.Boolean(
        string='Is Credit Note',
        compute='_compute_is_credit_note',
    )
    et_credit_reason = fields.Selection([
        ('goods_return', 'Goods Returned (የተመለሱ እቃዎች)'),
        ('price_correction', 'Price / Calculation Error (የዋጋ ወይም የስሌት ስህተት ማስተካከያ)'),
        ('post_sale_discount', 'Post-Sale Discount / Rebate (ከሽያጭ በኋላ የተሰጠ ቅናሽ)'),
        ('cancellation', 'Full Cancellation of Transaction (የግብይት መሰረዝ)'),
        ('other', 'Other Legal Reason (ሌላ ህጋዊ ምክንያት)'),
    ], string='MOR Legal Reason', tracking=True,
       help='Mandatory legal justification under Ethiopian VAT Proclamation No. 285/2002 Article 24')

    et_original_invoice_id = fields.Many2one(
        'account.move',
        string='Original Tax Invoice (ዋናው የግብር ደረሰኝ)',
        copy=False,
        domain="[('move_type', 'in', ('out_invoice', 'in_invoice')), ('state', '=', 'posted')]",
        help='The original tax invoice being adjusted or reversed by this credit note',
    )
    et_original_invoice_date = fields.Date(
        string='Original Invoice Date',
        related='et_original_invoice_id.invoice_date',
        readonly=True,
    )

    # Fiscal Cash Register (FCR / ESRM) Fields
    fcr_mrc = fields.Char(
        string='Machine Reg. Code (MRC)',
        copy=False,
        help='Electronic Sales Register Machine (ESRM) Code approved by Ministry of Revenues',
    )
    fcr_fs_no = fields.Char(
        string='Fiscal Slip No. (FS)',
        copy=False,
        help='Fiscal receipt/slip number issued by the cash register machine',
    )
    fcr_ej_no = fields.Char(
        string='Electronic Journal No. (EJ)',
        copy=False,
        help='Electronic journal audit trail number',
    )

    # Withholding Tax Fields
    wht_type = fields.Selection([
        ('goods', 'Supply of Goods (የእቃዎች አቅርቦት)'),
        ('services', 'Supply of Services (የአገልግሎቶች አቅርቦት)'),
        ('exempt', 'Exempt / Excluded (ነፃ / የማይመለከተው)'),
    ], string='WHT Category', default='goods', tracking=True,
       help='Category determining the statutory withholding threshold (Goods >= 10,000 ETB, Services >= 3,000 ETB)')

    wht_threshold = fields.Monetary(
        string='Applicable Threshold',
        compute='_compute_wht_status',
        currency_field='currency_id',
        help='Minimum statutory untaxed amount that triggers mandatory 2% Withholding Tax',
    )
    wht_threshold_exceeded = fields.Boolean(
        string='WHT Threshold Exceeded',
        compute='_compute_wht_status',
        help='True if the bill untaxed amount meets or exceeds the statutory threshold',
    )
    wht_applied = fields.Boolean(
        string='WHT Deducted',
        compute='_compute_wht_status',
        store=True,
        help='Indicates whether Withholding Tax (2%) is actively applied to the bill lines',
    )
    wht_rate = fields.Float(
        string='WHT Rate (%)',
        compute='_compute_wht_status',
    )
    wht_amount = fields.Monetary(
        string='Withheld Tax (2%)',
        compute='_compute_wht_status',
        currency_field='currency_id',
        store=True,
        help='Total amount withheld from supplier to be remitted to Ministry of Revenues',
    )
    wht_net_payable = fields.Monetary(
        string='Net Payable to Vendor',
        compute='_compute_wht_status',
        currency_field='currency_id',
        store=True,
        help='Actual amount to disburse to the supplier after 2% Withholding Tax deduction',
    )
    wht_warning = fields.Char(
        string='WHT Compliance Warning',
        compute='_compute_wht_warning',
    )

    # Official Ministry of Revenues (MOR) Withholding Tax Receipt Fields
    wht_receipt_number = fields.Char(
        string='WHT Receipt No.',
        copy=False,
        readonly=True,
        index=True,
        tracking=True,
        help='Official sequential Ethiopian Withholding Tax Certificate Number (የተቀናሽ ግብር ደረሰኝ ቁጥር)',
    )
    wht_receipt_date = fields.Date(
        string='WHT Certificate Date',
        copy=False,
        tracking=True,
        help='Date when the Withholding Tax Certificate was officially issued',
    )
    wht_manual_receipt_number = fields.Char(
        string='Manual Booklet Serial No.',
        copy=False,
        tracking=True,
        help='Pre-printed paper receipt booklet serial number if manually issued (የደረሰኝ ቁጥር ከመጽሐፍ)',
    )
    wht_certificate_issued = fields.Boolean(
        string='WHT Certificate Generated',
        copy=False,
        readonly=True,
        tracking=True,
    )
    wht_certificate_printed_count = fields.Integer(
        string='Receipt Print Count',
        default=0,
        copy=False,
    )
    wht_officer_name = fields.Char(
        string='Authorized Tax Officer',
        copy=False,
        help='Officer certifying the withholding on behalf of company (ያረጋገጠው ባለስልጣን ስም)',
    )
    wht_amount_words_en = fields.Char(
        string='WHT In Words (EN)',
        compute='_compute_wht_amount_words',
    )
    wht_amount_words_am = fields.Char(
        string='WHT In Words (AM)',
        compute='_compute_wht_amount_words',
    )

    @api.depends('wht_amount', 'currency_id')
    def _compute_wht_amount_words(self):
        for move in self:
            if move.wht_amount > 0:
                move.wht_amount_words_am = amount_to_amharic(move.wht_amount)
                move.wht_amount_words_en = move.currency_id.amount_to_text(move.wht_amount)
            else:
                move.wht_amount_words_am = False
                move.wht_amount_words_en = False

    @api.depends('move_type')
    def _compute_is_credit_note(self):
        for move in self:
            move.is_credit_note = move.move_type in ('out_refund', 'in_refund')

    @api.depends('move_type', 'amount_untaxed', 'wht_type', 'company_id', 'invoice_line_ids.tax_ids')
    def _compute_wht_status(self):
        for move in self:
            company = move.company_id
            wht_rate = company.et_wht_rate or 2.0
            move.wht_rate = wht_rate

            if move.move_type not in ('in_invoice', 'in_refund'):
                move.wht_threshold = 0.0
                move.wht_threshold_exceeded = False
                move.wht_applied = False
                move.wht_amount = 0.0
                move.wht_net_payable = move.amount_total
                continue

            # Determine threshold based on category
            if move.wht_type == 'services':
                threshold = company.et_wht_services_threshold or 3000.0
            elif move.wht_type == 'goods':
                threshold = company.et_wht_goods_threshold or 10000.0
            else:
                threshold = float('inf')

            move.wht_threshold = threshold
            is_exceeded = (move.amount_untaxed >= threshold) and (move.wht_type != 'exempt')
            move.wht_threshold_exceeded = is_exceeded

            # Check if any invoice line has WHT tax applied
            has_wht = False
            for line in move.invoice_line_ids:
                if any(tax.is_wht_tax for tax in line.tax_ids):
                    has_wht = True
                    break

            move.wht_applied = has_wht

            wht_calc = move.currency_id.round(move.amount_untaxed * (wht_rate / 100.0))
            if has_wht:
                move.wht_amount = wht_calc
                move.wht_net_payable = move.amount_total
            elif is_exceeded:
                # Show expected withheld amount even before applied
                move.wht_amount = wht_calc
                move.wht_net_payable = move.amount_total - wht_calc
            else:
                move.wht_amount = 0.0
                move.wht_net_payable = move.amount_total

    @api.depends('wht_threshold_exceeded', 'wht_applied', 'amount_untaxed', 'wht_threshold', 'state', 'move_type')
    def _compute_wht_warning(self):
        for move in self:
            if move.move_type == 'in_invoice' and move.state == 'draft' and move.wht_threshold_exceeded and not move.wht_applied:
                move.wht_warning = _(
                    "⚠️ Ministry of Revenues (MOR) Notice: This bill's untaxed total of %(amount)s %(curr)s "
                    "exceeds the %(threshold)s %(curr)s threshold. Click 'Apply WHT (2%%)' to deduct "
                    "Withholding Tax, or set category to 'Exempt' if supplier holds a valid exemption.",
                    amount=f"{move.amount_untaxed:,.2f}",
                    threshold=f"{move.wht_threshold:,.2f}",
                    curr=move.currency_id.symbol or move.currency_id.name or 'ETB',
                )
            else:
                move.wht_warning = False

    def action_apply_wht(self):
        """Automatically attaches the Ethiopian 2% WHT tax to all qualifying invoice lines."""
        for move in self:
            if move.move_type != 'in_invoice' or move.state != 'draft':
                continue
            company = move.company_id
            wht_tax = company.et_wht_tax_id or self.env['account.tax'].search([
                ('is_wht_tax', '=', True),
                ('type_tax_use', '=', 'purchase'),
                ('company_id', '=', company.id),
            ], limit=1)

            if not wht_tax:
                wht_tax = self.env.ref('l10n_et_tax.et_tax_purchase_wht_2', raise_if_not_found=False)

            if not wht_tax:
                raise UserError(_("No Withholding Tax (WHT) record found. Please configure it in Settings -> Invoicing."))

            for line in move.invoice_line_ids:
                if line.display_type in ('line_section', 'line_note'):
                    continue
                if wht_tax not in line.tax_ids:
                    line.tax_ids = [(4, wht_tax.id)]

    def action_remove_wht(self):
        """Removes Withholding Tax from all bill lines."""
        for move in self:
            if move.state != 'draft':
                continue
            for line in move.invoice_line_ids:
                wht_taxes = line.tax_ids.filtered(lambda t: t.is_wht_tax)
                if wht_taxes:
                    line.tax_ids = [(3, t.id) for t in wht_taxes]

    def action_generate_wht_receipt(self):
        """Generates the official sequential WHT Receipt number if not already present."""
        for move in self:
            if not move.wht_applied or move.move_type not in ('in_invoice', 'in_refund'):
                continue
            if not move.wht_receipt_number:
                seq = self.env['ir.sequence'].next_by_code('l10n_et_tax.wht.receipt')
                move.wht_receipt_number = seq or f"WHT/{fields.Date.today().year}/{move.id:05d}"
            if not move.wht_receipt_date:
                move.wht_receipt_date = move.invoice_date or fields.Date.context_today(move)
            if not move.wht_officer_name and move.company_id.et_wht_officer_name:
                move.wht_officer_name = move.company_id.et_wht_officer_name
            move.wht_certificate_issued = True

    def action_print_wht_receipt(self):
        """Generates receipt number if needed, increments print count, and returns PDF report."""
        self.ensure_one()
        if not self.wht_applied:
            raise UserError(_("No Withholding Tax is applied on this vendor bill."))
        self.action_generate_wht_receipt()
        self.wht_certificate_printed_count += 1
        return self.env.ref('l10n_et_tax.action_report_wht_receipt').report_action(self)

    def action_post(self):
        """Enforces Ethiopian Credit Note reason and logs audit trails."""
        for move in self:
            if move.is_credit_note and not move.et_credit_reason:
                raise ValidationError(_(
                    "Ethiopian Ministry of Revenues Compliance:\n"
                    "Please select the 'MOR Legal Reason' before confirming this Credit Note / Refund."
                ))
        res = super().action_post()
        for move in self:
            if move.move_type == 'in_invoice' and move.wht_applied:
                move.action_generate_wht_receipt()
                move.message_post(body=_(
                    "<b>Ethiopian Withholding Tax Deducted:</b><br/>"
                    "• Official WHT Receipt No: %(rcpt)s<br/>"
                    "• Rate: %(rate)s%%<br/>"
                    "• Amount Withheld: %(amount)s %(curr)s<br/>"
                    "• Net Payable to Vendor: %(net)s %(curr)s",
                    rcpt=move.wht_receipt_number or 'Pending',
                    rate=move.wht_rate,
                    amount=f"{move.wht_amount:,.2f}",
                    net=f"{move.wht_net_payable:,.2f}",
                    curr=move.currency_id.symbol or move.currency_id.name or 'ETB',
                ))
            elif move.is_credit_note and move.et_credit_reason:
                move.message_post(body=_(
                    "<b>Ethiopian Credit Note (MOR Article 24):</b><br/>"
                    "• Reason: %(reason)s<br/>"
                    "• Original Invoice: %(orig)s",
                    reason=dict(self._fields['et_credit_reason'].selection).get(move.et_credit_reason),
                    orig=move.et_original_invoice_id.name or 'N/A',
                ))
        return res
