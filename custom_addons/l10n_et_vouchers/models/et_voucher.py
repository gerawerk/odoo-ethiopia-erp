# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

try:
    from odoo.addons.l10n_et_tax.tools.amount_to_text_am import amount_to_amharic
except (ImportError, ModuleNotFoundError):
    try:
        import sys
        import os
        tools_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'l10n_et_tax', 'tools'))
        if tools_path not in sys.path:
            sys.path.insert(0, tools_path)
        from amount_to_text_am import amount_to_amharic
    except Exception:
        def amount_to_amharic(amount):
            return f"{amount:,.2f} ብር ብቻ"


class EtVoucher(models.Model):
    _name = 'et.voucher'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Ethiopian Financial Voucher (CPV, CRV, BPV, PCV)'
    _order = 'date desc, id desc'

    name = fields.Char(
        string='Voucher Number (የሰነድ ቁጥር)',
        default='/',
        copy=False,
        readonly=True,
        index=True,
        tracking=True,
        help='Unique sequential voucher number generated according to voucher type',
    )
    voucher_type = fields.Selection([
        ('cpv', 'Cash Payment Voucher (CPV / የጥሬ ገንዘብ ክፍያ)'),
        ('crv', 'Cash Receipt Voucher (CRV / የጥሬ ገንዘብ መቀበያ)'),
        ('bpv', 'Bank Payment Voucher (BPV / የባንክ ክፍያ / ቼክ)'),
        ('pcv', 'Petty Cash Voucher (PCV / የጥቃቅን ወጪ)'),
    ], string='Voucher Type (የሰነድ አይነት)', required=True, default='cpv', tracking=True)

    state = fields.Selection([
        ('draft', 'Draft (ረቂቅ)'),
        ('checked', 'Checked / Verified (የመረመረው)'),
        ('approved', 'Approved / Authorized (የፈቀደው)'),
        ('paid', 'Paid / Posted (የተከፈለ)'),
        ('cancelled', 'Cancelled (የተሰረዘ)'),
    ], string='Status (ሁኔታ)', default='draft', tracking=True, copy=False)

    date = fields.Date(
        string='Voucher Date (ቀን)',
        default=fields.Date.context_today,
        required=True,
        tracking=True,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Payee / Payer (ተከፋይ / ከፋይ)',
        tracking=True,
        help='The person or entity receiving or remitting the funds',
    )
    partner_tin_number = fields.Char(
        related='partner_id.tin_number',
        string='Partner TIN',
        readonly=True,
    )
    journal_id = fields.Many2one(
        'account.journal',
        string='Journal (የክፍያ ጆርናል)',
        required=True,
        tracking=True,
        domain="[('type', 'in', ('bank', 'cash')), ('company_id', '=', company_id)]",
        help='The cash safe or bank account source of disbursement/receipt',
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        related='company_id.currency_id',
        store=True,
        readonly=True,
    )
    narration = fields.Text(
        string='Payment Purpose / Memo (የክፍያው ምክንያት / ማብራሪያ)',
        tracking=True,
        help='Detailed description of the transaction and business justification',
    )

    # 4-Stage Signatory Audit Trail Fields
    prepared_by_id = fields.Many2one(
        'res.users',
        string='Prepared By (ያዘጋጀው)',
        default=lambda self: self.env.user,
        readonly=True,
        copy=False,
        tracking=True,
        help='Officer/Clerk who created the payment voucher and compiled receipts',
    )
    prepared_date = fields.Datetime(
        string='Date Prepared (የተዘጋጀበት ቀን)',
        default=fields.Datetime.now,
        readonly=True,
        copy=False,
    )
    checked_by_id = fields.Many2one(
        'res.users',
        string='Checked By (የመረመረው)',
        readonly=True,
        copy=False,
        tracking=True,
        help='Senior accountant / auditor who verified transaction documents and account codes',
    )
    checked_date = fields.Datetime(
        string='Date Checked (የተመረመረበት ቀን)',
        readonly=True,
        copy=False,
    )
    approved_by_id = fields.Many2one(
        'res.users',
        string='Approved By (የፈቀደው)',
        readonly=True,
        copy=False,
        tracking=True,
        help='Finance Manager / Executive who authorized the payment disbursement',
    )
    approved_date = fields.Datetime(
        string='Date Approved (የተፈቀደበት ቀን)',
        readonly=True,
        copy=False,
    )
    paid_by_id = fields.Many2one(
        'res.users',
        string='Paid / Disbursed By (የከፈለው/ገንዘብ ያዥ)',
        readonly=True,
        copy=False,
        tracking=True,
        help='Cashier or bank signatory who disbursed the cash or executed the bank transfer',
    )
    paid_date = fields.Datetime(
        string='Date Paid (የተከፈለበት ቀን)',
        readonly=True,
        copy=False,
    )
    rejection_reason = fields.Text(
        string='Rejection / Clarification Note (የውድቅ ምክንያት)',
        copy=False,
        tracking=True,
        help='Reason for rejecting the voucher back to draft for clarification',
    )

    # Bank Instrument Details (BPV)
    bank_payment_method = fields.Selection([
        ('cheque', 'Bank Cheque (ቼክ)'),
        ('cpo', 'Certified Payment Order (CPO)'),
        ('transfer', 'Electronic Bank Transfer (የባንክ ዝውውር)'),
        ('telebirr', 'Telebirr / Mobile Money (ቴሌብር)'),
        ('other', 'Other Bank Instrument (ሌላ)'),
    ], string='Bank Instrument', default='cheque', tracking=True)

    cheque_number = fields.Char(
        string='Cheque / CPO / Ref No. (የቼክ / CPO ቁጥር)',
        tracking=True,
        help='Official cheque leaf number, CPO reference, or bank transfer transaction ID',
    )
    cheque_date = fields.Date(
        string='Cheque Date (የቼክ ቀን)',
        tracking=True,
        help='Date printed on the cheque or date the bank transfer was executed',
    )
    payee_bank_id = fields.Many2one(
        'res.bank',
        string='Payee Bank (የተከፋይ ባንክ)',
        help='Beneficiary commercial bank name (e.g. Commercial Bank of Ethiopia, Awash Bank, Dashen Bank)',
    )
    payee_bank_account = fields.Char(
        string='Payee Account No. (የባንክ ሂሳብ ቁጥር)',
        help='Beneficiary bank account number for electronic transfers',
    )

    # Voucher Lines
    line_ids = fields.One2many(
        'et.voucher.line',
        'voucher_id',
        string='Voucher Lines (የክፍያ ዝርዝር)',
        copy=True,
    )

    # Totals and Amount in Words
    amount_total = fields.Monetary(
        string='Total Amount (ጠቅላላ ድምር)',
        compute='_compute_amount_total',
        store=True,
        currency_field='currency_id',
        tracking=True,
    )
    amount_in_words_am = fields.Char(
        string='Amount in Words (AM / በፊደል)',
        compute='_compute_amount_in_words',
        store=True,
    )
    amount_in_words_en = fields.Char(
        string='Amount in Words (EN)',
        compute='_compute_amount_in_words',
        store=True,
    )

    # Accounting Integration
    move_id = fields.Many2one(
        'account.move',
        string='Journal Entry (የሂሳብ መዝገብ)',
        readonly=True,
        copy=False,
        help='Underlying double-entry accounting transaction generated by this voucher',
    )

    @api.depends('line_ids.amount')
    def _compute_amount_total(self):
        for voucher in self:
            voucher.amount_total = sum(voucher.line_ids.mapped('amount'))

    @api.depends('amount_total', 'currency_id')
    def _compute_amount_in_words(self):
        for voucher in self:
            if voucher.amount_total > 0:
                voucher.amount_in_words_am = amount_to_amharic(voucher.amount_total)
                voucher.amount_in_words_en = voucher.currency_id.amount_to_text(voucher.amount_total)
            else:
                voucher.amount_in_words_am = 'ዜሮ ብር ብቻ'
                voucher.amount_in_words_en = 'Zero Birr Only'

    @api.onchange('voucher_type')
    def _onchange_voucher_type(self):
        """Defaults journal according to cash vs bank voucher type."""
        company = self.company_id or self.env.company
        if self.voucher_type == 'bpv':
            journal = self.env['account.journal'].search([
                ('type', '=', 'bank'),
                ('company_id', '=', company.id),
            ], limit=1)
        else:
            journal = self.env['account.journal'].search([
                ('type', '=', 'cash'),
                ('company_id', '=', company.id),
            ], limit=1)
        if journal:
            self.journal_id = journal

    def _get_sequence_code(self):
        """Returns the specific sequence code based on the voucher type."""
        seq_map = {
            'cpv': 'l10n_et_vouchers.seq_cpv',
            'crv': 'l10n_et_vouchers.seq_crv',
            'bpv': 'l10n_et_vouchers.seq_bpv',
            'pcv': 'l10n_et_vouchers.seq_pcv',
        }
        return seq_map.get(self.voucher_type, 'l10n_et_vouchers.seq_cpv')

    def action_check(self):
        """
        Stage 2: Checked / Verified (የመረመረው).
        Senior Accountant / Auditor verifies line items, supporting documents,
        and account distribution.
        """
        for voucher in self:
            if voucher.state != 'draft':
                raise UserError(_("Only draft vouchers can be submitted for checking."))
            if not voucher.line_ids:
                raise ValidationError(_("Please add at least one line item before submitting this voucher."))
            if voucher.amount_total <= 0:
                raise ValidationError(_("Total voucher amount must be strictly greater than zero."))

            voucher.checked_by_id = self.env.user
            voucher.checked_date = fields.Datetime.now()
            voucher.state = 'checked'
            voucher.message_post(body=_(
                "<b>Voucher Verified / Checked (የመረመረው):</b><br/>"
                "• Verified By: %(user)s<br/>"
                "• Date: %(date)s<br/>"
                "• Total Amount: <b>%(amt)s %(curr)s</b>",
                user=voucher.checked_by_id.name,
                date=voucher.checked_date.strftime('%Y-%m-%d %H:%M:%S'),
                amt=f"{voucher.amount_total:,.2f}",
                curr=voucher.currency_id.symbol or voucher.currency_id.name or 'ETB',
            ))

    def action_approve(self):
        """
        Stage 3: Approved / Authorized (የፈቀደው).
        Finance Manager / General Manager authorizes disbursement.
        Enforces executive approval threshold check.
        """
        for voucher in self:
            if voucher.state != 'checked':
                raise UserError(_("Voucher must be in 'Checked' state before it can be approved."))

            # Enforce threshold limit check
            threshold = voucher.company_id.voucher_approval_threshold or 50000.0
            if voucher.amount_total > threshold:
                is_manager = (
                    self.env.user.has_group('l10n_et_vouchers.group_voucher_manager') or
                    self.env.user.has_group('account.group_account_manager')
                )
                if not is_manager:
                    raise UserError(_(
                        "Executive Authorization Required:\n\n"
                        "This voucher amount (%(amt)s %(curr)s) exceeds the company threshold of %(thresh)s %(curr)s.\n"
                        "Under Ethiopian financial control rules, it strictly requires authorization by a Finance Manager / Director.",
                        amt=f"{voucher.amount_total:,.2f}",
                        thresh=f"{threshold:,.2f}",
                        curr=voucher.currency_id.symbol or voucher.currency_id.name or 'ETB',
                    ))

            voucher.approved_by_id = self.env.user
            voucher.approved_date = fields.Datetime.now()
            voucher.state = 'approved'
            voucher.message_post(body=_(
                "<b>Voucher Approved / Authorized (የፈቀደው):</b><br/>"
                "• Authorized By: %(user)s<br/>"
                "• Date: %(date)s",
                user=voucher.approved_by_id.name,
                date=voucher.approved_date.strftime('%Y-%m-%d %H:%M:%S'),
            ))

    def action_pay(self):
        """
        Stage 4: Paid / Disbursed (የከፈለው/ገንዘብ ያዥ).
        Cashier or bank signatory disburses funds, assigns sequential number,
        and posts the double-entry Journal Entry (account.move) to the General Ledger.
        """
        for voucher in self:
            if voucher.state != 'approved':
                raise UserError(_("Voucher must be authorized and in 'Approved' state before payment disbursement."))
            if not voucher.line_ids:
                raise ValidationError(_("Please add at least one line item before disbursing this voucher."))
            if voucher.amount_total <= 0:
                raise ValidationError(_("Total voucher amount must be strictly greater than zero."))

            # 1. Assign sequential voucher number
            if not voucher.name or voucher.name == '/':
                seq_code = voucher._get_sequence_code()
                voucher.name = self.env['ir.sequence'].next_by_code(seq_code) or f"{voucher.voucher_type.upper()}/{fields.Date.today().year}/{voucher.id:05d}"

            # 2. Determine Journal's default liquidity account
            liquidity_account = voucher.journal_id.default_account_id
            if not liquidity_account:
                payment_methods = voucher.journal_id.outbound_payment_method_line_ids.filtered(lambda p: p.payment_account_id)
                if payment_methods:
                    liquidity_account = payment_methods[0].payment_account_id

            if not liquidity_account:
                raise UserError(_(
                    "The selected journal '%s' has no default account configured. "
                    "Please configure a default account on the journal in Accounting Settings."
                ) % voucher.journal_id.name)

            # 3. Build Double-Entry Journal Lines
            # For Payments (CPV, BPV, PCV): Debit line accounts, Credit Liquidity account
            # For Receipts (CRV): Debit Liquidity account, Credit line accounts
            move_lines = []
            is_payment = voucher.voucher_type in ('cpv', 'bpv', 'pcv')

            # Liquidity aggregate line
            liquidity_line_vals = {
                'name': f"{voucher.name} - {voucher.narration or voucher.partner_id.name or ''}".strip(),
                'account_id': liquidity_account.id,
                'partner_id': voucher.partner_id.id if voucher.partner_id else False,
                'debit': 0.0 if is_payment else voucher.amount_total,
                'credit': voucher.amount_total if is_payment else 0.0,
            }
            move_lines.append((0, 0, liquidity_line_vals))

            # Breakdown lines from voucher lines
            for line in voucher.line_ids:
                line_vals = {
                    'name': line.name or voucher.narration or voucher.name,
                    'account_id': line.account_id.id,
                    'partner_id': line.partner_id.id if line.partner_id else (voucher.partner_id.id if voucher.partner_id else False),
                    'debit': line.amount if is_payment else 0.0,
                    'credit': 0.0 if is_payment else line.amount,
                }
                move_lines.append((0, 0, line_vals))

            # 4. Create and Post the account.move
            move_vals = {
                'move_type': 'entry',
                'journal_id': voucher.journal_id.id,
                'date': voucher.date,
                'ref': voucher.name,
                'line_ids': move_lines,
                'company_id': voucher.company_id.id,
            }
            move = self.env['account.move'].create(move_vals)
            move.action_post()

            voucher.move_id = move.id
            voucher.paid_by_id = self.env.user
            voucher.paid_date = fields.Datetime.now()
            voucher.state = 'paid'

            # 5. Log audit trail to chatter
            type_label = dict(self._fields['voucher_type'].selection).get(voucher.voucher_type)
            voucher.message_post(body=_(
                "<b>Ethiopian Financial Voucher Disbursed &amp; Paid (የተከፈለ):</b><br/>"
                "• Type: %(type)s<br/>"
                "• Number: <b>%(num)s</b><br/>"
                "• Total Amount: <b>%(amt)s %(curr)s</b><br/>"
                "• Disbursed By: %(user)s<br/>"
                "• In Words: <i>%(words_am)s</i><br/>"
                "• Journal Entry: %(move)s",
                type=type_label,
                num=voucher.name,
                amt=f"{voucher.amount_total:,.2f}",
                user=voucher.paid_by_id.name,
                curr=voucher.currency_id.symbol or voucher.currency_id.name or 'ETB',
                words_am=voucher.amount_in_words_am,
                move=move.name,
            ))

    def action_post(self):
        """Alias for action_pay to maintain backward compatibility."""
        return self.action_pay()

    def action_reject(self):
        """
        Rejects an in-review voucher back to Draft for clarification / correction.
        """
        for voucher in self:
            if voucher.state not in ('checked', 'approved'):
                raise UserError(_("Only vouchers in 'Checked' or 'Approved' status can be rejected."))
            voucher.state = 'draft'
            reason = voucher.rejection_reason or _("No reason provided.")
            voucher.message_post(body=_(
                "<b>Voucher Returned to Draft for Correction:</b><br/>"
                "• Reason / Clarification: %(reason)s<br/>"
                "• Returned By: %(user)s",
                reason=reason,
                user=self.env.user.name,
            ))

    def action_cancel(self):
        """Cancels voucher and reverses/unposts associated journal entry."""
        for voucher in self:
            if voucher.move_id and voucher.move_id.state == 'posted':
                voucher.move_id.button_cancel()
            voucher.state = 'cancelled'
            voucher.message_post(body=_("Voucher has been cancelled by %s.", self.env.user.name))

    def action_draft(self):
        """Resets cancelled voucher back to draft."""
        for voucher in self:
            if voucher.move_id and voucher.move_id.state == 'posted':
                raise UserError(_("Cannot reset to draft while journal entry is posted."))
            voucher.state = 'draft'

    def action_print_voucher(self):
        """Prints the official bilingual Ethiopian Financial Voucher PDF."""
        self.ensure_one()
        return self.env.ref('l10n_et_vouchers.action_report_et_voucher').report_action(self)

    def action_view_journal_entry(self):
        """Action for the smart button on form view opening the created journal entry."""
        self.ensure_one()
        return {
            'name': _('Journal Entry'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': self.move_id.id,
            'target': 'current',
        }


class EtVoucherLine(models.Model):
    _name = 'et.voucher.line'
    _description = 'Ethiopian Financial Voucher Line'

    voucher_id = fields.Many2one(
        'et.voucher',
        string='Voucher Reference',
        ondelete='cascade',
        required=True,
    )
    account_id = fields.Many2one(
        'account.account',
        string='Account (የሂሳብ መደብ)',
        required=True,
        domain="[('company_id', '=', company_id), ('deprecated', '=', False)]",
        help='Destination expense, asset, payable, receivable, or revenue account',
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner (አጋር)',
        help='Specific partner for this line if differing from overall voucher payee/payer',
    )
    name = fields.Char(
        string='Description / Particulars (ማብራሪያ)',
        required=True,
        help='Item description, service rendered, or payment purpose',
    )
    amount = fields.Monetary(
        string='Amount (መጠን)',
        required=True,
        currency_field='currency_id',
    )
    currency_id = fields.Many2one(
        'res.currency',
        related='voucher_id.currency_id',
        store=True,
        readonly=True,
    )
    company_id = fields.Many2one(
        'res.company',
        related='voucher_id.company_id',
        store=True,
        readonly=True,
    )
