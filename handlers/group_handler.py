import tornado.web
from .base_handler import BaseHandler
from models.group import Group
from models.user import User
from .util import check_group_permission


class GroupsHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        groupname = self.get_argument('group_name', '')
        groups = self.session.query(Group).filter(Group.name.ilike('%{0}%'.format(groupname))).order_by(Group.name).all()
        self.render('group/groups.html', groups=groups)

    @tornado.web.authenticated
    def post(self):
        name = self.get_argument('group_name', '')
        description = self.get_argument('description', '')
        group = Group(name=name, description=description)
        user_dict = self.get_current_user()
        user = self.session.query(User).filter_by(id=user_dict['id']).first()
        self.session.add(group)
        user.groups.append(group)
        self.session.commit()
        self.redirect(self.reverse_url('groups'))


class GroupHandler(BaseHandler):

    @check_group_permission
    @tornado.web.authenticated
    def get(self, group_id):
        group = self.session.query(Group).filter_by(id=group_id).first()
        self.render('group/group.html', group=group)


class GroupEditHandler(BaseHandler):

    @check_group_permission
    @tornado.web.authenticated
    def post(self, group_id):
        name = self.get_argument('group_name', '')
        description = self.get_argument('description', '')
        group = self.session.query(Group).filter_by(id=group_id).first()
        group.name = name
        group.description = description
        self.session.add(group)
        self.session.commit()
        self.redirect(self.reverse_url('group', group_id))


class GroupDeleteHandler(BaseHandler):

    @check_group_permission
    @tornado.web.authenticated
    def post(self, group_id):
        group = self.session.query(Group).filter_by(id=group_id).first()
        self.session.delete(group)
        self.session.commit()
        self.redirect(self.reverse_url('groups'))


class SearchNewMembersHandler(BaseHandler):

    @check_group_permission
    @tornado.web.authenticated
    def get(self, group_id):
        username = self.get_argument('username', '')
        users = self.session.query(User).filter(User.name.ilike('%{0}%'.format(username))).order_by(User.name).all()
        users = [user for user in users if not user.belongs_to_group(int(group_id))]
        group = self.session.query(Group).filter_by(id=group_id).first()
        self.render('group/search_new_members.html', users=users, group=group)

    @check_group_permission
    @tornado.web.authenticated
    def post(self, group_id):
        user_id = self.get_argument('uid', '')
        user = self.session.query(User).filter_by(id=user_id).first()
        group = self.session.query(Group).filter_by(id=group_id).first()
        user.groups.append(group)
        self.session.commit()
        self.redirect(self.reverse_url('search_new_members', group_id))

class GroupUserHandler(BaseHandler):

    @check_group_permission
    @tornado.web.authenticated
    def get(self, group_id):
        group = self.session.query(Group).filter_by(id=group_id).first()
        self.render('group/group_users.html', group=group)