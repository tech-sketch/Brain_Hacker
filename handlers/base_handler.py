import tornado.web
from backend import Backend


"""
class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    @property
    def session(self):
        return self.application.session_engine

    def on_finish(self):
        if self.session and self.session.is_modified:
            self.session.save()

        super(BaseHandler, self).on_finish()
"""

class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie('user')

    def set_current_user(self, username):
        self.set_secure_cookie('user', tornado.escape.utf8(username))

    def clear_current_user(self):
        self.clear_cookie(self.cookie_username)

    @property
    def session(self):
        return Backend.instance().get_session()