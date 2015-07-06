import tornado.web
import tornado.escape
from handlers.base_handler import BaseHandler
from models.user import User
from forms.forms import UserForm


class LoginHandler(BaseHandler):

    def get(self):
        self.render('auth/login.html', error_message='')

    def post(self):
        email = self.get_argument('email', '')
        password = self.get_argument('password', '')
        user = User.authenticate(email=email, password=password)
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

    def post(self):
        email = self.get_argument('email', '')
        form = UserForm(self.request.arguments)
        if not form.validate():
            self.render('auth/signup.html', error_message='', form=form)
        elif User.exists_email(email):
            error_message = '既に存在するメールアドレスです。'
            self.render('auth/signup.html', error_message=error_message, form=form)
        else:
            user = User(**form.data)
            user.save()
            self.redirect(self.reverse_url('login'))