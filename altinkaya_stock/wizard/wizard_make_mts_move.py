# -*- coding: utf-8 -*-
#
#Created on Oct 12, 2018
#
#@author: dogan
#

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools import float_compare


class MakeMtsMove(models.TransientModel):
    _name = 'make.mts.move'

    move_id = fields.Many2one('stock.move','Move', readonly=True)
    #cancel_production_ids = fields.Many2many('mrp.production',compute='_compute_productions', string='Productions to be canceled')
    #cancel_move_ids = fields.Many2many('stock.move',compute='_compute_productions', string='Productions to be canceled')
    
    #cancel_procurement_ids = fields.Many2many('procurement.order',string='Procurements to cancel', compute='_compute_procurements')
    
    
    #@api.one
    #def _compute_procurements(self):
    #    self.move_orig_ids.
    
    
    @api.multi
    def action_confirm(self):
        self.ensure_one()
        sale_order = self.move_id.sale_line_id.order_id
        order_state = sale_order.state
        invoice_state = self.move_id.invoice_state
        self.move_id._action_cancel()
        self.move_id.procure_method = 'make_to_stock'
        self.move_id.action_confirm()
        self.move_id.action_assign()
        
        if order_state != 'shipping_except' and sale_order.state == 'shipping_except':
            sale_order.state = order_state

        if invoice_state != self.move_id.invoice_state:
            self.move_id.invoice_state = invoice_state
                
        return {}

