import falcon
import json

from library_management.connection import conn
from library_management.Database.models import Members, Book_issue
from sqlobject.sqlbuilder import *


class MemberOperation:
    json_content = {}

    def validate_json(self, req):
        try:
            self.json_content = json.loads(req.stream.read())
            print("Valid Input JSON: {}".format(self.json_content))
            return True
        except ValueError as e:
            self.json_content = {}
            print("Invalid Input JSON")
            return False

    def on_get(self, req, resp):
        valid_date = self.validate_json(req)
        if valid_date:
            req_param = self.json_content
            print(req_param)

            member = Select(['id', 'member_name', 'city', 'membership_status'],
                            where=Members.q.membership_status == req_param['membership_status'])

            # member = Members.select(EXISTS(Select(['id', 'member_name', 'city', 'membership_status'],
            #                                       where=(Members.q.membership_status == req_param[
            #                                           'membership_status']))))

            query = conn.sqlrepr(member)
            rows = conn.queryAll(query)
            print(rows)

            if member:
                members = []
                for m in rows:
                    temp = {"id": m.id, "Name": m[1], "city": m[2], "membership_status": m[3]}
                    members.append(temp)

                # print(members)
                output = {
                    "members": members
                }

            resp.media = output

    def on_get_issue_status(self, req, resp):
        valid_data = self.validate_json(req)
        if valid_data:
            req_param = self.json_content
            member = Select(['id', 'member_name'], join=LEFTJOIN(Members, Book_issue,
                                                                 Members.q.id == Book_issue.q.member),
                            where=Book_issue.q.book_issue_status == req_param['book_issue_status'])
            query = conn.sqlrepr(member)
            rows = conn.queryAll(query)
            print(rows)

            if member:
                members = []
                for m in rows:
                    temp = {"id": m[0], "member_name": m[1]}
                    members.append(temp)

                output = {
                    "members": members
                }

                resp.media = output
