import sqlalchemy.orm.exc
from sqlalchemy.sql import exists
import tornado.web
import tornado.escape
from handlers.base_handler import BaseHandler
from models.user import User
from forms.forms import UserForm


class LoginHandler(BaseHandler):

    def get(self):
        self.render('auth/login.html', error_message='')

    def authenticate(self, email, password):
        try:
            user = self.session.query(User).filter_by(email=email).one()
            return user if user.verify_password(password=password) else None
        except sqlalchemy.orm.exc.NoResultFound:
            return None

    def post(self):
        email = self.get_argument('email', '')
        password = self.get_argument('password', '')
        user = self.authenticate(email=email, password=password)
        if user is not None:
            self.set_current_user(user)
            self.redirect(self.reverse_url(name='index'))
        else:
            error_message = 'ユーザ名かパスワードが間違っています。'
            self.render('auth/login.html', error_message=error_message)


class LogoutHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.clear_cookie('user')
        self.redirect(self.reverse_url(name='index'))


class SignupHandler(BaseHandler):

    def get(self):
        self.render('auth/signup.html', error_message='', form=UserForm())

    def exists_email(self, email):
        return self.session.query(exists().where(User.email == email)).scalar()

    def post(self):
        email = self.get_argument('email', '')
        form = UserForm(self.request.arguments)
        if not form.validate():
            error_message = '入力が正しくありません'
            self.render('auth/signup.html', error_message=error_message, form=form)
        elif self.exists_email(email):
            error_message = '既に存在するメールアドレスです。'
            self.render('auth/signup.html', error_message=error_message, form=form)
        else:
            self.session.add(User(**form.data))
            self.session.commit()
            self.redirect(self.reverse_url('login'))