from library_management.connection import conn
from sqlobject import SQLObject, StringCol, IntCol, ForeignKey, DatabaseIndex


class Fine(SQLObject):
    _connection = conn

    fine_range = IntCol(notNone=True)
    fine_amount = IntCol(notNone=True)

    def get_fine(self):
        return {
            "id": self.id,
            "fine_range": self.fine_range,
            "fine_amount": self.fine_amount
        }


Fine.createTable(ifNotExists=True)
