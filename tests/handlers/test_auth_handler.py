from unittest import mock
from urllib import parse
from tests.handlers.test_base import TestBase
import tornado.testing
import tornado.web
from tornado.options import options



class TestAuthHandlerBeforeLogin(TestBase):

    def test_get_request_index(self):
        test_url = '/'
        response = self.fetch(test_url, method='GET')
        # print(response)
        self.assertEqual(response.code, 200)

    def test_get_request_login(self):
        test_url = '/auth/login/'
        response = self.fetch(test_url, method='GET')
        self.assertEqual(response.code, 200)
        # print(response)

    def test_post_request_login(self):
        """
        """
        test_url = '/auth/login/'
        post_args = {'username': 'test',
                     'email': 'testr@test.co.jp',
                     'password': 'test'
                     }
        response = self.fetch(test_url, method='POST')
        # print(response)
        self.assertEqual(response.code, 200)

    def test_get_request_signup(self):
        test_url = '/auth/signup/'
        response = self.fetch(test_url, method='GET')
        self.assertEqual(response.code, 200)
    """
    def test_post_request_signup(self):

        # If settings['xsrf_cookies'] = True
        # this test code error

        test_url = '/auth/signup/'
        post_args = {'username': 'karateman',
                     'email': '1warrior@earth.co.jp',
                     'password': '10001000'
                     }
        response = self.fetch(test_url, method='POST',
                              body=parse.urlencode(post_args),
                              follow_redirects=False)
        print(response)
        self.assertEqual(response.code, 302)
        self.assertTrue(
            response.headers['Location'].startswith('/auth/login/'),
            "response.headers['Location'] did not ends with /auth/login/")
    """
    def test_get_request_logout(self):
        test_url = '/auth/logout/'
        response = self.fetch(test_url,  method='GET', follow_redirects=False)
        # print(response)
        self.assertEqual(response.code, 302)
        self.assertTrue(
            response.headers['Location'].startswith('/auth/login/'),
            "response.headers['Location'] did not ends with /auth/login/"
        )

