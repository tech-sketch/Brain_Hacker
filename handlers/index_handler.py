from .base_handler import BaseHandler


class IndexHandler(BaseHandler):

    def get(self):
        error_message = self.get_argument('error_message', '')
        self.render('index.html', error_message=error_message)

    def delete(self, *args, **kwargs):
        print("Hello Delete")