import tornado.testing
import tornado.web
from tornado.options import options

from urls import url_patterns

class TestBase(tornado.testing.AsyncHTTPTestCase):

    def setUp(self):
        super(TestBase, self).setUp()

    def get_app(self):
        settings = dict()
        tornado.web.Application(handlers=url_patterns, **settings)

    def get_http_port(self):
        return options.port
