from sqlobject import StringCol, SQLObject
from library_management.connection import conn


class User(SQLObject):
    _connection = conn

    username = StringCol(alternateID=True, length=20)
    password = StringCol(length=20)


User.createTable(ifNotExists=True)
