from library_management.connection import conn
from sqlobject import SQLObject, ForeignKey, StringCol, DateCol, IntCol
from library_management.Database.models.Book import Book
from library_management.Database.models.Members import Members
from library_management.Database.models.Fine_details import Fine


class BookIssue(SQLObject):
    _connection = conn

    date_issue = DateCol(notNone=True)
    date_return = DateCol(notNone=True)
    date_returned = DateCol(notNone=True)
    book_issue_status = StringCol(length=30)
    member = ForeignKey('Members', cascade=True)
    book = ForeignKey('Book', cascade=True)
    fine = ForeignKey('Fine', cascade=True)

    def get_book_issue_details(self):
        return {
            "date_issue": self.date_issue,
            "date_return": self.date_return,
            "date_returned": self.date_returned,
            "book_issue_status": self.book_issue_status
        }


BookIssue.createTable(ifNotExists=True)
