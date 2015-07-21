import tornado.web


class SearchBar(tornado.web.UIModule):
    def render(self, **kwargs):
        return self.render_string('modules/search_bar.html', **kwargs)


class DeleteModal(tornado.web.UIModule):
    def render(self, *args, **kwargs):
        return self.render_string('modules/delete_modal.html', **kwargs)


class EditModal(tornado.web.UIModule):
    def render(self, *args, **kwargs):
        Form = kwargs['Form']
        form = Form(prefix=kwargs['name'])
        names = [name for name in Form()._fields]
        for name in names:
            getattr(form, name).name = name
            getattr(form, name).data = getattr(kwargs['model'], name)
        kwargs['form'] = form
        return self.render_string('modules/edit_modal.html', **kwargs)


class CreateModal(tornado.web.UIModule):
    def render(self, *args, **kwargs):
        Form = kwargs['Form']
        form = Form(prefix=kwargs['name'])
        names = [name for name in Form()._fields]
        for name in names:
            getattr(form, name).name = name
        kwargs['form'] = form
        return self.render_string('modules/create_modal.html', **kwargs)
