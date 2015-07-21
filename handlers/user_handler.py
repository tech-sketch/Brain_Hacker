import tornado.web
from handlers.base_handler import BaseHandler
from models.user import User


class UsersHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        user_name = self.get_argument('user_name', '')
        users = User.search_name(user_name)
        self.render('user/users.html', users=users)


class UserHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, user_id):
        user = User.get(user_id)
        self.render('user/user.html', user=user)
