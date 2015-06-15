import tornado.web
from .base_handler import BaseHandler
from models.user import User

class UsersHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        users = self.session.query(User).all()
        self.render('users.html', users=users)

    @tornado.web.authenticated
    def post(self):
        username = self.get_argument('username', '')
        users = self.session.query(User).filter(User.name.like('%{0}%'.format(username))).all()
        self.render('users.html', users=users)


class UserHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, id):
        user = self.session.query(User).filter_by(id=id).first()
        self.render('user.html', user=user)