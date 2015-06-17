import tornado.web
from .base_handler import BaseHandler
from models.group import Group
from models.user import User

class GroupsHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        groupname = self.get_argument('groupname', '')
        groups = self.session.query(Group).filter(Group.name.like('%{0}%'.format(groupname))).all()
        self.render('group/groups.html', groups=groups)

    @tornado.web.authenticated
    def post(self):
        name = self.get_argument('name', '')
        group = Group(name=name)
        user_dict = self.get_current_user()
        user = self.session.query(User).filter_by(id=user_dict['id']).first()
        self.session.add(group)
        user.groups.append(group)
        self.session.commit()
        self.redirect(self.reverse_url('groups'))


class GroupHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, group_id):
        group = self.session.query(Group).filter_by(id=group_id).first()
        self.render('group/group.html', group=group)


class GroupEditHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, group_id):
        group = self.session.query(Group).filter_by(id=group_id).first()
        self.render('group/group_edit.html', group=group)

    @tornado.web.authenticated
    def post(self, group_id):
        method = self.get_argument('delete-confirmation', '')
        if method == "DELETE":
            self.delete(group_id)
        else:
            name = self.get_argument('name', '')
            group = self.session.query(Group).filter_by(id=group_id).first()
            group.name = name
            self.session.add(group)
            self.session.commit()
            self.redirect(self.reverse_url('group', group_id))

    @tornado.web.authenticated
    def delete(self, group_id):
        group = self.session.query(Group).filter_by(id=group_id).first()
        self.session.delete(group)
        self.session.commit()
        self.redirect(self.reverse_url('groups'))


class SearchNewMembersHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, group_id):
        username = self.get_argument('username', '')
        users = self.session.query(User).filter(User.name.like('%{0}%'.format(username))).all()
        users = [user for user in users if not user.belongs_to_group(int(group_id))]
        group = self.session.query(Group).filter_by(id=group_id).first()
        self.render('group/search_new_members.html', users=users, group=group)

    @tornado.web.authenticated
    def post(self, group_id):
        user_id = self.get_argument('uid', '')
        user = self.session.query(User).filter_by(id=user_id).first()
        group = self.session.query(Group).filter_by(id=group_id).first()
        user.groups.append(group)
        self.session.commit()
        self.redirect(self.reverse_url('search_new_members', group=group))

class GroupUserHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, group_id):
        group = self.session.query(Group).filter_by(id=group_id).first()
        self.render('group/group_users.html', group=group)