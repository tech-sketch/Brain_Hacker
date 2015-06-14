from .base_handler import BaseHandler


class IndexHandler(BaseHandler):

    def get(self):
        self.render('index.html')