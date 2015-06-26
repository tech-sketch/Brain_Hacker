import tornado.web
import tornado.escape
from backend import Backend


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json:
            return None
        return tornado.escape.json_decode(user_json)

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie('user', tornado.escape.json_encode(user.json()))
        else:
            self.clear_cookie('user')

    def clear_current_user(self):
        self.clear_cookie('user')

    @property
    def session(self):
        return Backend.instance().get_session()