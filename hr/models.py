
from osv import orm, fields


class Employee(orm.Model):

    _inherit = 'hr.employee'

    _columns = {
        'insurance_number': fields.integer('Numero de seguro')
    }

    def create(self, cr, user, vals, context=None):
        employee_id = super(Employee, self).create(cr, user, vals, context)
        return employee_id

    def write(self, cr, user, ids, vals, context=None):
        return super(Employee, self).write(cr, user, ids, vals, context)

    def unlink(self, cr, uid, ids, context=None):
        return super(Employee, self).unlink(cr, uid, ids, context)
