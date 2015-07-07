import tornado.web
from handlers.base_handler import BaseHandler
from models.group import Group
from models.user import User
from .util import check_group_permission
from forms.forms import GroupForm


class GroupsHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        group_name = self.get_argument('group_name', '')
        groups = Group.search_name(group_name)
        self.render('group/groups.html', groups=groups)

    @tornado.web.authenticated
    def post(self):
        form = GroupForm(self.request.arguments)
        if form.validate():
            group = Group(**form.data)
            user_id = self.get_current_user_id()
            user = User.get(user_id)
            user.groups.append(group)
            group.save()
            self.redirect(self.reverse_url('group', group.id))
        else:
            self.redirect(self.reverse_url('groups'))  # Todo エラーメッセージを渡す


class GroupHandler(BaseHandler):

    @check_group_permission
    @tornado.web.authenticated
    def get(self, group_id):
        group = Group.get(group_id)
        self.render('group/group.html', group=group)


class GroupEditHandler(BaseHandler):

    @check_group_permission
    @tornado.web.authenticated
    def post(self, group_id):
        form = GroupForm(self.request.arguments)
        if form.validate():
            group = Group.get(group_id)
            group.update(**form.data)
            group.save()
            self.redirect(self.reverse_url('group', group_id))
        else:
            self.redirect(self.reverse_url('group', group_id))


class GroupDeleteHandler(BaseHandler):

    @check_group_permission
    @tornado.web.authenticated
    def post(self, group_id):
        Group.get(group_id).delete()
        self.redirect(self.reverse_url('groups'))


class GroupMemberAdditionHandler(BaseHandler):

    @check_group_permission
    @tornado.web.authenticated
    def get(self, group_id):
        user_name = self.get_argument('user_name', '')
        users = User.search_name(user_name)
        users = [user for user in users if not user.belongs_to_group(group_id)]
        group = Group.get(group_id)
        self.render('group/member_addition.html', users=users, group=group)

    @check_group_permission
    @tornado.web.authenticated
    def post(self, group_id):
        user_id = self.get_argument('user_id', '')
        user = User.get(user_id)
        group = Group.get(group_id)
        user.groups.append(group)
        user.save()
        self.redirect(self.reverse_url('member_addition', group_id))


class GroupUserHandler(BaseHandler):

    @check_group_permission
    @tornado.web.authenticated
    def get(self, group_id):
        group = Group.get(group_id)
        self.render('group/group_users.html', group=group)