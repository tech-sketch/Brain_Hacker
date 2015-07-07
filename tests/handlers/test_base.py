import tornado.testing
import tornado.web
import tornado.escape

from tornado.options import options

from urls import url_patterns
from urllib import parse

class TestBase(tornado.testing.AsyncHTTPTestCase):

    def setUp(self):
        super(TestBase, self).setUp()

    def get_app(self):
        self.app = tornado.web.Application(handlers=url_patterns, xsrf_cookies=False)

    def get_http_port(self):
        return options.port

    def user_login(self):
        login_url = '/auth/login/'
        post_args = {'email': 'test@test.co.jp',
                     'password': 'test'
                     }
        response = self.fetch(login_url, method='POST',
                              body=parse.urlencode(post_args),
                              follow_redirects=False)
        return response

    def user_logout(self):
        test_url = '/auth/logout/'
        response = self.fetch(test_url,  method='GET', follow_redirects=False)
        return response
