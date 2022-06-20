from library_management.connection import conn
from sqlobject import SQLObject, ForeignKey, StringCol, IntCol, DateCol


class Members(SQLObject):
    _connection = conn

    member_name = StringCol(length=50, notNone=True)
    city = StringCol(length=50)
    date_register = DateCol(notNone=True)
    date_expire = DateCol(notNone=True)
    membership_status = StringCol(length=50)

    def get_member(self):
        return {
            "id": self.id,
            "member_name": self.member_name,
            "city": self.city,
            "date_register": self.date_register,
            "date_expire": self.date_expire,
            "membership_status": self.membership_status
        }


Members.createTable(ifNotExists=True)
