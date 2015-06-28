import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import options

from urls import url_patterns
from settings import settings


class Application(tornado.web.Application):

    def __init__(self):
        tornado.web.Application.__init__(self, handlers=url_patterns, **settings)


def main():
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
        tornado.ioloop.IOLoop.instance().stop()