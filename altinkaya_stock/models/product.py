
from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.category'

    currency_id = fields.Many2one(
        string='Currency', readonly=False, comodel_name='res.currency')

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    def _compute_currency_id(self):
        main_company = self.env['res.company']._get_main_company()
        for template in self:
            if template.categ_id.currency_id:
                template.currency_id = template.categ_id.currency_id.id
            else:
                template.currency_id = template.company_id.sudo().currency_id.id or main_company.currency_id.id

    @api.multi
    def _compute_cost_currency_id(self):
        main_company = self.env['res.company']._get_main_company()
        for template in self:
            if template.categ_id.currency_id:
                template.cost_currency_id = template.categ_id.currency_id.id
            else:
                template.cost_currency_id = template.company_id.sudo().currency_id.id or main_company.currency_id.id

    @api.multi
    def _guess_main_lang(self):
        super(ProductTemplate, self)._guess_main_lang()
        turkish = self.env.ref('base.lang_tr')
        if turkish.active:
            code = turkish.code
        else:
            code = self.env['res.lang'].search([], limit=1).code
        return code

class Product(models.Model):
    _inherit = "product.product"

    domain_attribute_value_ids = fields.Many2many('product.attribute.value', compute='_compute_domain_attribute_value_ids')

    @api.multi
    @api.depends('product_tmpl_id', 'product_tmpl_id.valid_product_attribute_value_ids')
    def _compute_domain_attribute_value_ids(self):
        for product in self:
            product.domain_attribute_value_ids = product.product_tmpl_id.attribute_line_ids.mapped('value_ids')

    qty_available_sincan = fields.Float('Sincan Depo Mevcut',compute='_compute_custom_available', search='_search_qty_sincan')
    qty_available_merkez = fields.Float('Merkez Depo Mevcut',compute='_compute_custom_available', search='_search_qty_merkez')
    qty_available_enjek = fields.Float('Enjeksiyon Depo Mevcut',compute='_compute_custom2_available', search='_search_qty_enjek')
    qty_available_montaj = fields.Float('Montaj Depo Mevcut',compute='_compute_custom2_available', search='_search_qty_montaj')
    qty_available_cnc = fields.Float('CNC Depo Mevcut', compute='_compute_custom2_available',
                                        search='_search_qty_cnc')
    qty_available_metal = fields.Float('Metal Depo Mevcut', compute='_compute_custom2_available',
                                        search='_search_qty_metal')
    qty_available_boya = fields.Float('Boya Depo Mevcut', compute='_compute_custom2_available',
                                       search='_search_qty_boya')
    qty_available_maske = fields.Float('Maske Depo Mevcut', compute='_compute_custom2_available',
                                       search='_search_qty_maske')

    qty_incoming_sincan = fields.Float('Sincan Depo Gelen',compute='_compute_custom_available')
    qty_incoming_merkez = fields.Float('Merkez Depo Gelen',compute='_compute_custom_available')
    qty_outgoing_sincan = fields.Float('Sincan Depo Giden',compute='_compute_custom_available')
    qty_outgoing_merkez = fields.Float('Merkez Depo Giden',compute='_compute_custom_available')
    qty_virtual_sincan = fields.Float('Sincan Depo Tahmini',compute='_compute_custom_available')
    qty_virtual_merkez = fields.Float('Merkez Depo Tahmini',compute='_compute_custom_available')


    # active_bom =  fields.Many2one('mrp.bom', string='Active Bom',
    #     compute='_find_active_bom', readonly=True, store=False)
    #
    # routing_id = fields.Many2one('mrp.routing', string='Rota',
    #     related='active_bom.routing_id',readonly=True)
    #
    # @api.one
    # def _find_active_bom(self):
    #     self.active_bom = self.pool.get('mrp.bom')._bom_find(self._cr, self._uid, product_id=self.id,
    #                                                          product_tmpl_id=self.product_tmpl_id.id)

    
#    type_variant = fields.Selection([('product','Stockable Product'),('consu','Consumable'),('service','Service')], string="Product Type", default=False,store=True)
#    type = fields.Selection([('product','Stockable Product'),('consu','Consumable'),('service','Service')],compute='_compute_type')
    
    
#    @api.multi
#    def _compute_type(self):
#        for product in self:
#            product.type = product.type_variant or product.product_tmpl_id.type
            
    
    def _search_qty_merkez(self, operator, value):
        return [('id', 'in', self.with_context({'location':12})._search_qty_available(operator, value))]
                 
    def _search_qty_sincan(self, operator, value):
        return [('id', 'in', self.with_context({'location':21})._search_qty_available(operator, value))]

    def _search_qty_enjek(self, operator, value):
        return [('id', 'in', self.with_context({'location':28})._search_qty_available(operator, value))]

    def _search_qty_montaj(self, operator, value):
        return [('id', 'in', self.with_context({'location':52})._search_qty_available(operator, value))]

    def _search_qty_cnc(self, operator, value):
        return [('id', 'in', self.with_context({'location':60})._search_qty_available(operator, value))]

    def _search_qty_boya(self, operator, value):
        return [('id', 'in', self.with_context({'location':44})._search_qty_available(operator, value))]

    def _search_qty_metal(self, operator, value):
        return [('id', 'in', self.with_context({'location':36})._search_qty_available(operator, value))]

    def _search_qty_maske(self, operator, value):
        return [('id', 'in', self.with_context({'location':114})._search_qty_available(operator, value))]


    @api.multi
    def _compute_custom_available(self):
        for product in self:
            product.qty_available_sincan = product.with_context({'location':21}).qty_available
            product.qty_available_merkez = product.with_context({'location':12}).qty_available
            product.qty_incoming_sincan = product.with_context({'location':21}).incoming_qty
            product.qty_incoming_merkez = product.with_context({'location':12}).incoming_qty
            product.qty_outgoing_sincan = product.with_context({'location':21}).outgoing_qty
            product.qty_outgoing_merkez = product.with_context({'location':12}).outgoing_qty
            product.qty_virtual_sincan = product.with_context({'location':21}).virtual_available
            product.qty_virtual_merkez = product.with_context({'location':12}).virtual_available

    @api.multi
    def _compute_custom2_available(self):
        for product in self:
            product.qty_available_montaj = product.with_context({'location':53}).qty_available
            product.qty_available_enjek = product.with_context({'location':28}).qty_available
            product.qty_available_cnc = product.with_context({'location':60}).qty_available
            product.qty_available_boya = product.with_context({'location':44}).qty_available
            product.qty_available_metal = product.with_context({'location':36}).qty_available
            product.qty_available_maske = product.with_context({'location':114}).qty_available
            
            





class mrpProduction(models.Model):
    _inherit = "mrp.production"

    qty_available_sincan = fields.Float('Sincan Depo Mevcut', related='product_id.qty_available_sincan')
    qty_available_merkez = fields.Float('Merkez Depo Mevcut', related='product_id.qty_available_merkez')
    qty_available_enjek = fields.Float('Enjeksiyon Depo Mevcut', related='product_id.qty_available_enjek')
    qty_available_montaj = fields.Float('Montaj Depo Mevcut', related='product_id.qty_available_montaj')
    qty_available_cnc = fields.Float('CNC Depo Mevcut', related='product_id.qty_available_cnc')
    qty_available_metal = fields.Float('Metal Depo Mevcut', related='product_id.qty_available_metal')
    qty_available_boya = fields.Float('Boya Depo Mevcut',related='product_id.qty_available_boya')
    qty_available_maske = fields.Float('Maske Depo Mevcut', related='product_id.qty_available_maske')

