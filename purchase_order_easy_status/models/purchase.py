# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnuorg/licenses/agpl.html).

from odoo import api, fields, models, _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _default_easy_state(self):
        if self:
            easy_sate = False
            if not isinstance(self.id, models.NewId):
                easy_sate = self.env['easy.state'].search([('model', '=', 'sale.order'), ('sate'), '=', self.state], limit=1)
            if not easy_sate:
                easy_sate = 'open'
            return easy_sate

    easy_state = fields.Selection([
        ('open', 'Open purchase'),
        ('finished', 'Purchase is Closed/Finished'),
        ('cancel', 'Canceled')], string='Easy status',
        default=lambda self: self._default_easy_state())

    @api.onchange('state')
    def _onchange_state(self):
        for purchase in self:
            if not isinstance(purchase.id, models.NewId):
                easy_sate = self.env['easy.state'].search([('model', '=', 'purchase.order'), ('sate'), '=', purchase.state], limit=1)
                if easy_sate:
                    purchase.easy_state = easy_sate
                else:
                    purchase.easy_state = 'open'
