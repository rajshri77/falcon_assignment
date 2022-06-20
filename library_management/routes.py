import falcon
from library_management.resources.services.login import Login
from library_management.resources.services.Book import BookService
from library_management.resources.services.Book_issue import BookIssueService
from library_management.resources.services.Members import MembersService
from library_management.resources.services.Suppliers import SuppliersService
from library_management.resources.services.Fine import FineService
from library_management.resources.services.Operations import MemberOperation


def get_app():
    app = falcon.App()
    app.add_route("/login", Login())
    app.add_route("/Book", BookService())
    app.add_route("/Book_issue", BookIssueService())
    app.add_route("/Members", MembersService())
    app.add_route("/Suppliers", SuppliersService())
    app.add_route("/Fine", FineService())
    app.add_route("/q1", MemberOperation())
    return app
