from odoo import api, fields, models

class SalePack(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        super(SalePack, self).action_confirm()
        for line in self.order_line:
            if line.product_id.is_pack:
                for record in line.product_id.pack_products_ids:
                    dest_loc = self.env.ref('stock.stock_location_customers').id
                    self.env['stock.move'].create({
                        'name': record.product_id.name,
                        'product_id': record.product_id.id,
                        'product_uom_qty': record.quantity * line.product_uom_qty,
                        'product_uom': record.product_id.uom_id.id,
                        'picking_id': self.picking_ids[0].id,
                        'location_id': self.picking_ids.picking_type_id.default_location_src_id.id,
                        'location_dest_id': dest_loc,
                    })
