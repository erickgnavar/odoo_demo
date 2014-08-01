# coding: utf-8


from osv import orm, fields, osv


class Service(orm.Model):

    _name = 'mydemo.service'

    _columns = {
        'name': fields.char('Nombre')
    }


class MyModel(orm.Model):

    _name = 'mydemo.mymodel'

    _columns = {
        'name': fields.char('Name', required=True),
        'quantity': fields.integer('Cantidad'),
        'type': fields.selection(selection=(
            ('single', 'Unico'),
            ('multiple', 'Multiple')
        ), string='Tipo'),
        'state': fields.selection(selection=(
            ('draft', 'Borrador'),
            ('sent', 'Enviado'),
            ('approved', 'Aprovado'),
            ('rejected', 'Rechazado')
        )),
        'department_id': fields.many2one('hr.department', string='Departamento'),
        'employee_id': fields.many2one('hr.employee', string='Empleado'),
        'supplier_id': fields.many2one('res.partner', string='Proveedor'),
        'detail_ids': fields.one2many('mydemo.mymodel.detail', 'my_model_id'),
        'employee_ids': fields.many2many('hr.employee', string='Empleados'),
        'service_ids': fields.many2many('mydemo.service', string='Servicios')
    }

    _defaults = {
        'type': 'single',
        'state': 'draft'
    }

    def action_sent(self, cr, uid, ids, context=None):
        # raise osv.except_osv('Alerta', 'No tiene permisos para enviar')
        self.write(cr, uid, ids, {
            'state': 'sent'
        })
        return True

    def action_approved(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {
            'state': 'approved'
        })
        return True

    def action_rejected(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {
            'state': 'rejected'
        })
        return True

    def on_change_department_id(self, cr, uid, ids, department_id, context=None):
        return {
            'domain': {
                'employee_id': [('department_id', '=', department_id)]
            }
        }


class MyModelDetail(orm.Model):

    _name = 'mydemo.mymodel.detail'

    def _calculate_total(self, cr, uid, ids, field_name, args=None, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            res[record.id] = record.quantity * record.price
        return res

    _columns = {
        'my_model_id': fields.many2one('mydemo.mymodel'),
        'number': fields.integer('Numero'),
        'name': fields.char('Nombre'),
        'price': fields.float('Precio'),
        'quantity': fields.integer('Cantidad'),
        'total': fields.function(_calculate_total, store=True, type='float',
                                 method=True, string='Total'),
        'product_id': fields.many2one('product.product', string='Producto')
    }

    def on_change_product_id(self, cr, uid, ids, product_id, context=None):
        if not product_id:
            return {
                'value': {}
            }
        product = self.pool.get('product.product').read(cr, uid, product_id, ['name'])
        name = product['name']
        return {
            'value': {
                'name': name
            }
        }

    def on_change_quantity_or_price(self, cr, uid, ids, quantity, price, context=None):
        return {
            'value': {
                'total': quantity * price
            }
        }
