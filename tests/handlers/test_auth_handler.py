from urllib import parse
from tests.handlers.test_base import TestBase

from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
from urls import url_patterns
from settings import settings
from urllib.parse import urlencode
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user import User

"""
Test user value
post_args = {
                'username': 'test',
                'email': 'test@test.co.jp',
                'password': 'test'
            }

"""
class TestAuthHandlerBeforeLogin(TestBase):

    def test_get_request_index(self):
        test_url = '/'
        response = self.fetch(test_url, method='GET')
        self.assertEqual(response.code, 200)

    def test_post_request_index(self):
        # Bad Request
        test_url = '/'
        post_args = {}
        response = self.fetch(test_url, method='POST',body=parse.urlencode(post_args))
        self.assertEqual(response.code, 405)

    def test_get_request_login(self):
        test_url = '/auth/login/'
        response = self.fetch(test_url, method='GET')
        self.assertEqual(response.code, 200)

    def test_post_request_login(self):
        print("login post")
        test_url = '/auth/login/'

        post_args = {'email': 'test@test.co.jp',
                     'password': 'test'
                     }

        response = self.fetch(test_url, method='POST',
                              body=parse.urlencode(post_args),
                              follow_redirects=False,
                              )
        # print(response)
        self.assertEqual(response.code, 302)
        self.assertTrue(
            response.headers['Location'] == '/',
            "response.headers['Location'] did not ends with /"
        )

    def test_get_request_signup(self):
        test_url = '/auth/signup/'
        response = self.fetch(test_url, method='GET')
        self.assertEqual(response.code, 200)
    """
    def test_get_and_post_request_signup(self):
        test_url = '/auth/signup/'
        post_args = {'username': 'karateman7',
                     'email': '1ar@earth.co.jp',
                     'password': '10001000'
                     }
        response = self.fetch(test_url, method='POST',
                              body=parse.urlencode(post_args),
                              follow_redirects=False,
                              )
        print(response)
        self.assertEqual(response.code, 302)
        self.assertTrue(
            response.headers['Location'].startswith('/auth/login/'),
            "response.headers['Location'] did not ends with /auth/login/")
    """
    def test_get_request_logout(self):
        # Bad Request
        print("logout get")
        test_url = '/auth/logout/'
        response = self.fetch(test_url,  method='GET', follow_redirects=False)
        # print(response)
        self.assertEqual(response.code, 302)
        self.assertTrue(
            response.headers['Location'].startswith('/auth/login/'),
            "response.headers['Location'] did not ends with /auth/login/"
        )

    """
     test_post_wrong_email_login(self):
        input in forms
        post_args = {
                'email': 'wrong_test@test.co.jp',
                'password': 'test'
            }
        We can observed by error message
    """

    """
     test_post_wrong_password_login(self):
        input in forms
        post_args = {
                'email': 'test@test.co.jp',
                'password': 'wrong'
            }
        We can observed by error message
    """

class TestAuthHandlerAfterLogin(TestBase):

    def test_get_request_index(self):
        print("login")
        response = self.user_login()
        user_cookie = response.headers['Set-Cookie']

        test_url = '/'
        response = self.fetch(test_url, method='GET', headers={'Cookie': user_cookie})
        print(response)
        self.assertEqual(response.code, 200)
    """
    def test_get_request_login(self):
        response = self.user_login()
        user_cookie = response.headers['Set-Cookie']

        test_url = '/auth/login/'
        response = self.fetch(test_url, method='GET', headers={'Cookie': user_cookie})
        self.assertEqual(response.code, 403)
        # We can observed by status 200
    """
    def test_get_request_logout(self):

        response = self.user_login()
        user_cookie = response.headers['Set-Cookie']

        test_url = '/auth/logout/'
        response = self.fetch(test_url,  method='GET', follow_redirects=False,
                              headers={'Cookie': user_cookie})
        # print(response)
        self.assertEqual(response.code, 302)
        self.assertTrue(
            response.headers['Location'] == '/',
            "response.headers['Location'] did not ends with /"
        )


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
