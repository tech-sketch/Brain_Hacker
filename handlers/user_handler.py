import tornado.web
from .base_handler import BaseHandler
from models.user import User

class UsersHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        username = self.get_argument('user_name', '')
        users = self.session.query(User).filter(User.name.ilike('%{0}%'.format(username))).order_by(User.name).all()
        self.render('user/users.html', users=users)


class UserHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, user_id):
        user = self.session.query(User).get(user_id)
        self.render('user/user.html', user=user)