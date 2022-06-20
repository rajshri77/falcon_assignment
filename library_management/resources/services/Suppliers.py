import falcon
import json
from sqlobject.sqlbuilder import Update
from library_management.Database.models.Suppliers_details import Suppliers


class SuppliersService:
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
            supplier = Suppliers(supplier_name=req_param['supplier_name'], address=req_param['address'],
                                 contact=req_param['contact'], email=req_param['email'])
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
            supplier = Suppliers.select(Suppliers.q.id == req_param['supp_id'])
        else:
            supplier = Suppliers.select()

        if supplier:
            suppliers = []
            for s in supplier:
                temp = {"supplier_id": s.id, "supplier_name": s.supplier_name, "address": s.address,
                        "contact": s.contact, "email": s.email}
                suppliers.append(temp)

                output = {
                    "suppliers": suppliers
                }

                resp.media = output

    def on_put(self, req, resp):
        valid_data = self.validate_json(req)
        if valid_data:
            req_param = self.json_content
            supplier = Suppliers.select(Suppliers.q.id == req_param['id'])
            supplier[0].supplier_name = req_param['supplier_name']

        print("Name updated..")
        output = {
            "msg": "Supplier name updated"
        }

        resp.media = output

    def on_delete(self, req, resp):
        valid_data = self.validate_json(req)
        if valid_data:
            req_param = self.json_content
            Suppliers.delete(req_param['id'])
        else:
            raise falcon.HTTPBadRequest(title="Please provide valid data", description="Invalid data! try again")

        output = {
            "msg": "Record Deleted"
        }

        resp.media = output
