from sqlobject import ForeignKey, StringCol, SQLObject, IntCol, DateCol
from library_management.connection import conn
from library_management.Database.models.Suppliers_details import Suppliers


class Book(SQLObject):
    _connection = conn

    title = StringCol(length=200)
    category = StringCol(length=50)
    author = StringCol(notNone=True)
    publication = StringCol(notNone=True)
    publish_date = DateCol(notNone=True)
    price = IntCol(notNone=True)
    supplier = ForeignKey('Suppliers')

    def get_book(self):
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "author": self.author,
            "publication": self.publication,
            "publish_date": self.publish_date,
            "price": self.price,
        }


Book.createTable(ifNotExists=True)
