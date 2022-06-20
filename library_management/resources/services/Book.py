import datetime

import falcon
from bson import json_util
import json
from sqlobject.sqlbuilder import Update
from library_management.Database.models.Book import Book


class BookService:
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

    def on_get(self, req, resp):
        valid_data = self.validate_json(req)
        if valid_data:
            req_params = self.json_content
            book = Book.select(Book.q.id == req_params["b_id"])
        else:
            book = Book.select()

        if book:
            books = []
            for b in book:
                temp = {"title": b.title, "category": b.category, "author": b.author, "publication": b.publication,
                        "publish_date": self.datetime_handler(b.publish_date), "price": b.price, "supplier": b.supplier.get_suppliers_details()["supplier_id"]}
                books.append(temp)

        output = {
                "Books": books
        }
        resp.media = output

    def datetime_handler(self, pdate):
        print(type(pdate))
        if isinstance(pdate, datetime.date):
            return pdate.isoformat()
        raise TypeError("Unknown type")

    def on_post(self, req, resp):
        valid_data = self.validate_json(req)
        if valid_data:
            req_param = self.json_content
            book = Book(title=req_param['title'], category=req_param['category'], author=req_param['author'],
                        publication=req_param['publication'], publish_date=req_param['publish_date'],
                        price=req_param['price'], supplier=req_param['supplier_id'])
        else:
            raise falcon.HTTPBadRequest(title="Please provide valid data", description="Invalid data! try again")

        output = {
            "msg": "Record Inserted"
        }

        resp.media = output

    def on_put(self, req, resp):
        valid_data = self.validate_json(req)
        if valid_data:
            req_param = self.json_content
            book = Book.select(Book.q.id == req_param['b_id'])
            book[0].title = req_param['title']

        print("Title Updated")
        output = {
            "msg": "Book title updated"
        }

        resp.media = output

    def on_delete(self, req, resp):
        valid_data = self.validate_json(req)
        if valid_data:
            req_params = self.json_content
            Book.delete(req_params['id'])
        else:
            raise falcon.HTTPBadRequest(title="Please provide valid data", description="Invalid data! try again")

        output = {
            "msg": "Record deleted"
        }

        resp.media = output
