import json
import falcon
from sqlobject.sqlbuilder import Update

from library_management.models.Author import Author


class Author:

    json_content = {}

    def validate__json(self, req):
        try:
            self.json_content = json.loads(req.stream.read())
            print("Valid Input JSON : {}".format(self.json_content))
            return True
        except ValueError as e:
            self.json_content = {}
            print("Invalid Input JSON")
            return False

    def on_get(self, req, resp):
        valid_data = self.validate__json(req)
        if valid_data:
            req_params = self.json_content
            author = Author.select(Author.q.id == req_params["id"])
        else:
            author = Author.select()

        if author:
            authors = []
            for a in author:
                auth = {"name": a.name}
                authors.append(auth)

        output = {
            "Authors": authors
        }

        resp.media = output

    def on_put(self, req, resp):

        valid_data = self.validate__json(req)
        if valid_data:
            req_params = self.json_content
            author = Update('Author', values={'name': req_params['name']}, where={'id': req_params['id']})

        print("Name Updated")
        output = {
            "msg": "Author name updated"
        }
        resp.media = output

    def on_delete(self, req, resp):
        valid_data = self.validate__json()
        if valid_data:
            req_params = self.json_content
            Author.delete(req_params["id"])
        else:
            raise falcon.HTTPBadRequest(title="Please provide valid data", description="Invalid data! try again")

        output = {
            "msg": "Record deleted"
        }

        resp.media = output

    def on_post(self, req, resp):
        valid_data = self.validate__json(req)
        if valid_data:
            req_params = self.json_content
            author = Author(name=req_params["name"])
        else:
            raise falcon.HTTPBadRequest(title="Please provide valid data", description="Invalid data! try again")

        print("Record Inserted!")

        output = {
            "msg": "Record Inserted"
        }

        resp.media = output
