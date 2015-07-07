from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
from urls import url_patterns
from settings import settings
from urllib.parse import urlencode
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user import User

class MyHTTPTest(AsyncHTTPTestCase):

    def get_app(self):
        return Application(url_patterns, **settings)
    """
    def test_index(self):
        response = self.fetch('/')

    def test_login(self):
        response = self.fetch('/auth/login/')
    """
    def test_login_post(self):

        post_args = {'name': 'yamada',
                 'email': 'yamada@tis.co.jp',
                 'password': 'yamada'
                 }
        body = urlencode(post_args)
        response = self.fetch('/auth/login/', method='POST', body=body, follow_redirects=True)
        print(response)