import tornado.testing
import tornado.web
import tornado.escape

from tornado.options import options
from http import cookies

import os
from urls import url_patterns
from urllib import parse

from settings import settings


class TestBase(tornado.testing.AsyncHTTPTestCase):
    """
    def __init__(self, *rest):
        self.cookies = cookies.SimpleCookie()
        tornado.testing.AsyncHTTPTestCase.__init__(self, *rest)
    def _update_cookies(self, headers):
        '''
        from
        https://github.com/peterbe/tornado-utils/blob/master/tornado_utils/http_test_client.py
        '''
        try:
            sc = headers['Set-Cookie']
            cookies = tornado.escape.native_str(sc)
            self.cookies.update(cookies.SimpleCookie(cookies))
            while True:
                self.cookies.update(cookies.SimpleCookie(cookies))
                if ',' not in cookies:
                    break
                cookies = cookies[cookies.find(',') + 1:]
        except KeyError:
            return

    def fetch(self, url, *r, **kw):
        if 'follow_redirects' not in kw:
            kw['follow_redirects'] = False
        header = {}
        hs = self.cookies.output()
        if hs != '':
            hs = hs.split(':')[1]
            header['Cookie'] = hs
        resp = tornado.testing.AsyncHTTPTestCase.fetch(self, url, headers=header, *r, **kw)
        self._update_cookies(resp.headers)
        return resp
    """


    def setUp(self):
        super(TestBase, self).setUp()

    def get_app(self):
        #settings = dict()
        self.app = tornado.web.Application(handlers=url_patterns, **settings)

    def get_http_port(self):
        return options.port

    def user_login(self):
        login_url = '/auth/login/'
        post_args = {'username': 'test',
                     'email': 'test@test.co.jp',
                     'password': 'test'
                     }
        response = self.fetch(login_url, method='POST',
                              body=parse.urlencode(post_args),
                              follow_redirects=False)
        return response

    def user_logout(self, user_cookie):
        test_url = '/auth/logout/'
        response = self.fetch(test_url,  method='GET', follow_redirects=False)
        return response
