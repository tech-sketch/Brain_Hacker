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
        from tornado.options import options
        url = str(options.port) + self.reverse_url('room_socket', group_id, room_id)
        self.render('room/room.html', url=url)

class RoomEditHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, group_id, room_id):
        group = self.session.query(Group).filter_by(id=group_id).first()
        room = self.session.query(Room).filter_by(id=room_id).first()
        self.render('room/room_edit.html', group=group, room=room)

    @tornado.web.authenticated
    def post(self, group_id, room_id):
        name = self.get_argument('name', '')
        room = self.session.query(Room).filter_by(id=room_id).first()
        room.name = name
        self.session.add(room)
        self.session.commit()
        self.redirect(self.reverse_url('rooms', group_id))


class RoomDeleteHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self, group_id, room_id):
        room = self.session.query(Room).filter_by(id=room_id).first()
        self.session.delete(room)
        self.session.commit()
        self.redirect(self.reverse_url('rooms', group_id))

from tornado.ioloop import PeriodicCallback
class RoomSocketHandler(tornado.websocket.WebSocketHandler):

    #index.htmlでコネクションが確保されると呼び出される
    def open(self, *args, **kwargs):
        self.i = 0
        self.callback = PeriodicCallback(self._send_message, 400) #遅延用コールバック
        self.callback.start()
        print("WebSocket opened")

    #クライアントからメッセージが送られてくると呼び出される
    def on_message(self, message):
        print(message)
        import tornado.escape
        message_dict = tornado.escape.json_decode(message)
        if message_dict['action'] == 'create':
            self.write_message(message)
        elif message_dict['action'] == 'move':
            self.write_message(message)
        elif message_dict['action'] == 'delete':
            self.write_message(message)
        else:
            pass
        self.i = 0

    #コールバックスタートで呼び出しが始まる
    def _send_message(self):
        self.i += 1
        self.write_message(str(self.i))

    #ページが閉じ、コネクションが切れる事で呼び出し
    def on_close(self):
        self.callback.stop()
        print("WebSocket closed")