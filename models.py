# coding: utf-8


from osv import orm, fields


class MyModel(orm.Model):

    _name = 'mydemo.mymodel'

    _columns = {
        'name': fields.char('Name'),
        'quantity': fields.integer('Cantidad')
    }
