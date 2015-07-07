from unittest import mock
from urllib import parse
from tests.handlers.test_base import TestBase
from pprint import pprint
from handlers.base_handler import BaseHandler
from http import cookies
from tornado.testing import AsyncHTTPClient
from handlers.auth_handler import LogoutHandler
import tornado.testing
import tornado.web
from tornado.options import options

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
