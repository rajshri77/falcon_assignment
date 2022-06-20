import falcon
import json
import base64
from sqlobject.sqlbuilder import Select, AND, EXISTS
from library_management.Database.models.User import User


class Login:
    def __init__(self):
        pass

    def login(self, req, resp):
        req_params = json.loads(req.stream.read())
        print(req_params)
        if not req_params or not req_params["Username"] or not req_params["Password"]:
            raise falcon.HTTPBadRequest("Bad Request", "Please enter Username and Password")
        else:
            self.authenticate(req_params["Username"], req_params["Password"], resp)

    def authenticate(self, username, password, resp):
        if not username or not password:
            raise falcon.HTTPBadRequest("Bad Request", "Please enter valid username and password")
        elif not self.is_user_valid(username, password):
            raise falcon.HTTPUnauthorized("Unauthorized", "Invalid Credentials")
        else:
            user_id = User.select(EXISTS(Select(User.q.id, where=(User.q.username == username))))
            if user_id:
                user_id = str(user_id)
                id_bytes = user_id.encode('ascii')
                base64_bytes = base64.b64encode(id_bytes)
                resp.media = {"token": base64_bytes.decode('utf-8')}
                print("Authenticated Successfully...")

            else:
                resp.media = {"Error": "User Not Found"}
                resp.status = falcon.HTTP_200
            print("User Authenticated.....!")

    def is_user_valid(self, username, password):
        print("Username: {} and Password: {}".format(username, password))
        user_data = User.select(AND(User.q.username == username, User.q.password == password))
        print(user_data.count())
        if user_data.count() > 0:
            return True
        else:
            return False

    def on_post(self, req, resp):
        self.login(req, resp)


def main():
    pass


if __name__ == "__main__": main()
