import falcon
import json
import datetime
from sqlobject.sqlbuilder import Update
from library_management.Database.models.Book_issue import BookIssue


class BookIssueService:
    json_content = {}

    def validate_json(self, req):
        try:
            self.json_content = json.loads(req.stream.read())
            print("Valid Input JSON : {}".format(self.json_content))
            return True
        except ValueError as e:
            self.json_content = {}
            print("Invalid Input JSON")
            return False

    def on_post(self, req, resp):
        valid_data = self.validate_json(req)
        if valid_data:
            req_param = self.json_content
            BookIssue(date_issue=req_param['date_issue'], date_return=req_param['date_return'],
                      date_returned=req_param['date_returned'], book_issue_status=req_param['issue_status'],
                      member=req_param['member'], book=req_param['book'], fine=req_param['fine'])

        else:
            raise falcon.HTTPBadRequest(title="Please provide valid data", description="Invalid data! try again")

        output = {
            "msg": "Record Inserted"
        }

        resp.media = output

    def on_get(self, req, resp):
        valid_data = self.validate_json(req)
        if valid_data:
            req_param = self.json_content
            book_issue = BookIssue.select(BookIssue.q.id == req_param['bi_id'])
        else:
            book_issue = BookIssue.select()

        if book_issue:
            book_issues = []
            for b in book_issue:
                temp = {"date_issue": self.datetime_handler(b.date_issue),
                        "date_return": self.datetime_handler(b.date_return),
                        "date_returned": self.datetime_handler(b.date_returned),
                        "book_issue_status": b.book_issue_status, "member": b.member.get_member()['id'],
                        "book": b.book.get_book()['id'], "fine": b.fine.get_fine()['id']}
                book_issues.append(temp)

        output = {
            "book_issues": book_issues
        }

        resp.media = output

    def datetime_handler(self, pdate):
        print(type(pdate))
        if isinstance(pdate, datetime.date):
            return pdate.isoformat()
        raise TypeError("Unknown type")

    def on_put(self, req, resp):
        valid_data = self.validate_json(req)
        if valid_data:
            req_param = self.json_content
            book_issue = BookIssue.select(BookIssue.q.id == req_param['id'])
            book_issue[0].book_issue_status = req_param["book_issue_status"]

        print("Status Updated...")
        output = {
            "msg": "Book issue status updated.."
        }

        resp.media = output

    def on_delete(self, req, resp):
        valid_data = self.validate_json(req)
        if valid_data:
            req_param = self.json_content
            BookIssue.delete(req_param['id'])
        else:
            raise falcon.HTTPBadRequest(title="Please provide valid data", description="Invalid data! try again")

        output = {
            "nsg": "Record deleted..."
        }

        resp.media = output
