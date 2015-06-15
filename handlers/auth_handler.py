import sqlalchemy.orm.exc
import bcrypt
import tornado.web
import tornado.escape
from .base_handler import BaseHandler
from models.user import User


def is_authenticated(password, hashed_password):
    return bcrypt.hashpw(password=password.encode('utf-8'), salt=hashed_password) == hashed_password


class LoginHandler(BaseHandler):
    def get(self):
        try:
            error_message = self.get_argument('error')
        except:
            error_message = ''
        self.render('login.html', error_message=error_message)

    def check_permission(self, password, email):
        try:
            user = self.session.query(User).filter_by(email=email).one()
        except (sqlalchemy.orm.exc.NoResultFound, sqlalchemy.orm.exc.MultipleResultsFound):
            return False, None
        if is_authenticated(password, user.hashed_password):
            return True, user
        return False, None

    def post(self):
        email = self.get_argument('email', '')
        password = self.get_argument('password', '')
        auth, user = self.check_permission(password, email)
        if auth:
            self.set_current_user(user)
            self.redirect(self.reverse_url(name='index'))
        else:
            self.render('login.html', error_message='Login Incorrect')

    def set_current_user(self, user):
        if user:
            user_dict = {'name': user.name, 'email': user.email, 'id': user.id}
            self.set_secure_cookie('user', tornado.escape.json_encode(user_dict))
        else:
            self.clear_cookie('user')


class LogoutHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.clear_cookie('user')
        self.redirect(self.reverse_url(name='index'))


class SignupHandler(BaseHandler):
    def get(self):
        try:
            error_message = self.get_argument('error')
        except:
            error_message = ''
        print(id(self.session))
        self.render('signup.html', error_message=error_message)

    def can_regist(self, email):
        try:
            user = self.session.query(User).filter_by(email=email).one()
        except (sqlalchemy.orm.exc.NoResultFound):
            return True
        return False

    def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        email    = self.get_argument('email', '')
        if self.can_regist(email):
            hashed_password = bcrypt.hashpw(password=password.encode('utf-8'), salt=bcrypt.gensalt())
            self.session.add(User(name=username, hashed_password=hashed_password, email=email))
            self.session.commit()
            self.redirect(self.reverse_url('login'))
        else:
            error_message = 'E-Mail Address already exists!'
            self.render('signup.html', error_message=error_message)
