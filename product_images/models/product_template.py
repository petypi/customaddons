# -*- coding: utf-8 -*-
# © 2014-2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ProductTemplate(models.Model):
    
    _inherit = 'product.template'
     
    image_tmpl_ids = fields.One2many('ir.attachment', 'product_tmpl_id',domain=[('product_id','=',False)], string='Product Images')
