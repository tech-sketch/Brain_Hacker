import tornado.websocket
from .base_handler import BaseHandler
from models.room import Room
from models.group import Group


class RoomsHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, group_id):
        room_name = self.get_argument('room_name', '')
        rooms = self.session.query(Group).filter(Group.name.like('%{0}%'.format(room_name))).all()
        group = self.session.query(Group).filter_by(id=group_id).first()
        self.render('room/rooms.html', rooms=rooms, group=group)

    @tornado.web.authenticated
    def post(self, group_id):
        name = self.get_argument('name', '')
        room = Room(name=name)
        group = self.session.query(Group).filter_by(id=group_id).first()
        self.session.add(room)
        group.rooms.append(room)
        self.session.commit()
        self.redirect(self.reverse_url('rooms', group_id))


class RoomHandler(BaseHandler):

    def get(self, group_id, room_id):
        self.render('room/room.html')


class RoomSocketHandler(tornado.websocket.WebSocketHandler):
    pass