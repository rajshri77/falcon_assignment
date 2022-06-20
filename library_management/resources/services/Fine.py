import falcon
import json
from sqlobject.sqlbuilder import Update
from library_management.Database.models.Fine_details import Fine


class FineService:
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
            fine = Fine(fine_range=req_param['fine_range'], fine_amount=req_param['fine_amount'])
        else:
            raise falcon.HTTPBadRequest(title="Please provide valid data", description="Invalid data! try again")

        output = {
            "msg": "Record Inserted"
        }

        resp.media = output

    def on_get(self, req, resp):
        valid_date = self.validate_json(req)
        if valid_date:
            req_param = self.json_content
            fine = Fine.select(Fine.q.id == req_param["f_id"])
        else:
            fine = Fine.select()

        if fine:
            fines = []
            for f in fine:
                temp = {"fine_range": f.fine_range, "fine_amount": f.fine_amount}
                fines.append(temp)

        output = {
            "fine": fines
        }

        resp.media = output

    def on_put(self, req, resp):
        valid_data = self.validate_json(req)
        if valid_data:
            req_param = self.json_content
            fine = Fine.select(Fine.q.id == req_param['id'])
            fine[0].fine_amount = req_param['fine_amount']

        print("Fine amount updated...")
        output = {
            "msg": "Fine amount Updated..."
        }

        resp.media = output

    def on_delete(self, req, resp):
        valid_data = self.validate_json(req)
        if valid_data:
            req_param = self.json_content
            Fine.delete(req_param['id'])
        else:
            raise falcon.HTTPBadRequest(title="Please provide valid data", description="Invalid data! try again")

        output = {
            "msg": "Record deleted.."
        }

        resp.media = output
