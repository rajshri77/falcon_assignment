import datetime

import falcon
import json
from sqlobject.sqlbuilder import Update
from library_management.Database.models.Members import Members


class MembersService:
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
            Members(member_name=req_param['member_name'], city=req_param['city'],
                    date_register=req_param['date_register'], date_expire=req_param['date_expire'],
                    membership_status=req_param['membership_status'])

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
            member = Members.select(Members.q.id == req_param['m_id'])
        else:
            member = Members.select()

        if member:
            members = []
            for m in member:
                temp = {"member_id": m.id, "member_name": m.member_name, "city": m.city,
                        "date_register": self.datetime_handler(m.date_register),
                        "date_expire": self.datetime_handler(m.date_expire), "membership_status": m.membership_status}
                members.append(temp)

            output = {
                "member": members
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
            member = Members.select(Members.q.id == req_param['id'])
            member[0].member_name = req_param['member_name']

        print("Name updated...")
        output = {
            "msg": "Member name updated...."
        }

        resp.media = output

    def on_delete(self, req, resp):
        valid_data = self.validate_json(req)
        if valid_data:
            req_param = self.json_content
            Members.delete(req_param['id'])
        else:
            raise falcon.HTTPBadRequest(title="Please provide valid data", description="Invalid data! try again")

        output = {
            "msg": "Record deleted..."
        }

        resp.media = output
