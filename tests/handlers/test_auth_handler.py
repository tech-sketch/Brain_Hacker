from unittest import mock
from urllib import parse
from tests.handlers.test_base import TestBase
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

    def test_get_request_login(self):
        test_url = '/auth/login/'
        response = self.fetch(test_url, method='GET')
        self.assertEqual(response.code, 200)
    """
    def test_post_request_login(self):
        test_url = '/auth/login/'
        post_args = {'username': 'test',
                     'email': 'test@test.co.jp',
                     'password': 'test'
                     }
        resp = self.fetch(test_url, method='POST', body=parse.urlencode(post_args), follow_redirects=False)
        print(resp)
        self.assertEqual(200, resp.code)
    """
    def test_post_request_login(self):
        print("login post")
        test_url = '/auth/login/'

        response = self.fetch(test_url, method='GET')
        print(response.headers)
        cookies = response.headers['Set-Cookie']

        post_args = {'username': 'test',
                     'email': 'test@test.co.jp',
                     'password': 'test',
                     '_xsrf': cookies
                     }

        response = self.fetch(test_url, method='POST',
                              body=parse.urlencode(post_args),
                              follow_redirects=False,
                              )

        print(response)
        self.assertEqual(response.code, 302)

        self.assertTrue(
            response.headers['Location'] == '/',
            "response.headers['Location'] did not ends with /"
        )
    """
    def test_get_and_post_request_signup(self):
        test_url = '/auth/signup/'
        response = self.fetch(test_url, method='GET')
        print("GET")
        print(response.headers['Set-Cookie'])
        self.assertEqual(response.code, 200)

        with mock.patch(BaseHandler, 'get_secure_cookie') as m:
            json = BaseHandler.get_current_user(self)

        print(json)

        xsrf_cookies = response.headers['Set-Cookie']

        post_args = {'username': 'karateman7',
                     'email': '1ar@earth.co.jp',
                     'password': '10001000'
                     }
        response = self.fetch(test_url, method='POST',
                              body=parse.urlencode(post_args),
                              follow_redirects=False,
                              headers={'Cookie': xsrf_cookies})
        print(response)
        self.assertEqual(response.code, 302)
        self.assertTrue(
            response.headers['Location'].startswith('/auth/login/'),
            "response.headers['Location'] did not ends with /auth/login/")

    def test_get_request_logout(self):
        test_url = '/auth/logout/'
        response = self.fetch(test_url,  method='GET', follow_redirects=False)
        # print(response)
        self.assertEqual(response.code, 302)
        self.assertTrue(
            response.headers['Location'].startswith('/auth/login/'),
            "response.headers['Location'] did not ends with /auth/login/"
        )
"""

class TestAuthHandlerAfterLogin(TestBase):

    def test_get_request_index(self):
        response = self.user_login()
        user_cookie = response.headers['Set-Cookie']

        test_url = '/'
        response = self.fetch(test_url, method='GET', headers={'Cookie': user_cookie})
        # print(response)
        self.assertEqual(response.code, 200)

    def test_get_request_login(self):
        response = self.user_login()
        user_cookie = response.headers['Set-Cookie']

        test_url = '/auth/login/'
        response = self.fetch(test_url, method='GET', headers={'Cookie': user_cookie})
        self.assertEqual(response.code, 200)

    def test_post_request_logout(self):

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
