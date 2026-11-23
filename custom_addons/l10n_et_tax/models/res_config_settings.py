# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    et_tin_number = fields.Char(
        related='company_id.et_tin_number',
        readonly=False,
    )
    et_vat_reg_number = fields.Char(
        related='company_id.et_vat_reg_number',
        readonly=False,
    )
    et_sub_city = fields.Char(
        related='company_id.et_sub_city',
        readonly=False,
    )
    et_woreda = fields.Char(
        related='company_id.et_woreda',
        readonly=False,
    )
    et_house_number = fields.Char(
        related='company_id.et_house_number',
        readonly=False,
    )
    et_wht_enabled = fields.Boolean(
        related='company_id.et_wht_enabled',
        readonly=False,
    )
    et_wht_goods_threshold = fields.Monetary(
        related='company_id.et_wht_goods_threshold',
        readonly=False,
    )
    et_wht_services_threshold = fields.Monetary(
        related='company_id.et_wht_services_threshold',
        readonly=False,
    )
    et_wht_rate = fields.Float(
        related='company_id.et_wht_rate',
        readonly=False,
    )
    et_wht_tax_id = fields.Many2one(
        related='company_id.et_wht_tax_id',
        readonly=False,
    )
    et_tot_goods_tax_id = fields.Many2one(
        related='company_id.et_tot_goods_tax_id',
        readonly=False,
    )
    et_tot_services_tax_id = fields.Many2one(
        related='company_id.et_tot_services_tax_id',
        readonly=False,
    )
