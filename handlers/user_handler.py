from .base_handler import BaseHandler


class UsersHandler(BaseHandler):

    def get(self):
        self.render('index.html')


class UserHandler(BaseHandler):
    pass