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
            errormessage = self.get_argument("error")
        except:
            errormessage = ""
        self.render("login.html", error_message = errormessage)

    def check_permission(self, password, email):
        user = self.session.query(User).filter_by(email=email).first()
        print(user.hashed_password)
        print(type(user.hashed_password))
        print(password)
        print(is_authenticated(password, user.hashed_password))
        return True
        user = self.session.query(User).filter_by(email=email.encode('utf-8')).first()
        print(user.name)

        #if is_authenticated(password, user.hashed_password):
            #return True
        #return False

    def post(self):
        email = self.get_argument('email', '')
        password = self.get_argument('password', '')
        auth = self.check_permission(password, email)
        if auth:
            self.set_current_user(email)
            self.redirect(self.reverse_url(name='index'))
        else:
            self.render('login.html', error_message='Login Incorrect')
            #self.redirect(self.reverse_url(name='login'))
            #error_msg = u"?error=" + tornado.escape.url_escape("Login incorrect")
            #self.redirect(u"/login/" + error_msg)

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie('user', tornado.escape.json_encode(user))
        else:
            self.clear_cookie('user')


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.reverse_url(name='index'))


class SignupHandler(BaseHandler):
    def get(self):
        try:
            error_message = self.get_argument("error")
        except:
            error_message = ""
        print(id(self.session))
        self.render("signup.html", error_message=error_message)

    def __register(self, password, username, email):
        username = username
        password = password
        email = email
        # DBにメールアドレスが存在する場合False

        hashed_password = bcrypt.hashpw(password=password.encode('utf-8'), salt=bcrypt.gensalt())
        # validation and store db
        return True

    def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        email    = self.get_argument('email', '')
        hashed_password = bcrypt.hashpw(password=password.encode('utf-8'), salt=bcrypt.gensalt())
        self.session.add(User(name=username, hashed_password=hashed_password, email=email))
        self.session.commit()
        #new = self.__register(password, username, email)
