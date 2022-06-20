import falcon
from library_management.connection import conn
import base64
from library_management.Database.models import User


class Auth:

    def process_request(self, req, resp):
        if '/login' in req.path:
            return
        if req.get_header('Autherization'):
            token = req.get_header('Autherization').split(" ")
            token = token[1]
        else:
            msg = "Missing autherization header"
            raise falcon.HTTPUnauthorized("Unautherized", msg)

        print("Token: {}".format(token))
        if not token:
            msg = "Please provide the token"
            raise falcon.HTTPUnauthorized("Unautherized", msg)
        if not self.token_is_valid(token):
            try:
                base64_string = base64.b64decode(token)
                print(base64_string)
                user_id = User.select(User.q.user_id == base64_string["user_id"])
                if user_id[0] == base64_string[1]:

                    print("Authenticated User : {}", format(user_id))
                    return True
            except UnicodeDecodeError:
                return False
