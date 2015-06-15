import tornado.web
from .base_handler import BaseHandler


class GroupsHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render('groups.html', groups=[])


class GroupHandler(BaseHandler):
    pass


class GroupUserHandler(BaseHandler):
    pass