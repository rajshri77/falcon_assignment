from library_management.connection import conn
from sqlobject import SQLObject, StringCol, IntCol


class Suppliers(SQLObject):
    _connection = conn

    supplier_name = StringCol(length=100, notNone=True)
    address = StringCol(length=100)
    contact = IntCol(length=10)
    email = StringCol(length=50)

    def get_suppliers_details(self):
        return {
            "supplier_id": self.id,
            "supplier_name": self.supplier_name,
            "address": self.address,
            "contact": self.contact,
            "email": self.email
        }


Suppliers.createTable(ifNotExists=True)
