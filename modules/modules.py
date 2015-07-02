import tornado.web


class SearchBar(tornado.web.UIModule):
    def render(self, **kwargs):
        return self.render_string('modules/search_bar.html', **kwargs)