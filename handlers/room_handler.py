import json
import random
import uuid

import tornado.web
import tornado.websocket
from tornado import gen
from tornado.web import asynchronous

from .base_handler import BaseHandler
from models.room import Room
from models.group import Group
from .rooms import Rooms
from .util import check_group_permission
from forms.forms import RoomForm


class RoomsHandler(BaseHandler):

    @check_group_permission
    @tornado.web.authenticated
    def get(self, group_id):
        room_name = self.get_argument('room_name', '')
        rooms = self.session.query(Room).filter(Room.name.ilike('%{0}%'.format(room_name))).filter_by(group_id=group_id).order_by(Room.name).all()
        group = self.session.query(Group).filter_by(id=group_id).first()
        self.render('room/rooms.html', rooms=rooms, group=group)

    @check_group_permission
    @tornado.web.authenticated
    def post(self, group_id):
        form = RoomForm(self.request.arguments)
        if form.validate():
            room = Room(**form.data)
            group = self.session.query(Group).filter_by(id=group_id).first()
            self.session.add(room)
            group.rooms.append(room)
            self.session.commit()
        self.redirect(self.reverse_url('rooms', group_id))


class RoomHandler(BaseHandler):

    @check_group_permission
    @tornado.web.authenticated
    def get(self, group_id, room_id):
        from tornado.options import options
        port = str(options.port)
        room = self.session.query(Room).filter_by(id=room_id).first()
        self.render('room/room.html', room_id=room_id, port=port, theme=room.theme)


class RoomEditHandler(BaseHandler):

    @check_group_permission
    @tornado.web.authenticated
    def post(self, group_id, room_id):
        form = RoomForm(self.request.arguments)
        if form.validate():
            room = self.session.query(Room).filter_by(id=room_id).first()
            room.update(**form.data)
            self.session.add(room)
            self.session.commit()
        self.redirect(self.reverse_url('rooms', group_id))


class RoomDeleteHandler(BaseHandler):

    @check_group_permission
    @tornado.web.authenticated
    def post(self, group_id, room_id):
        room = self.session.query(Room).filter_by(id=room_id).first()
        self.session.delete(room)
        self.session.commit()
        self.redirect(self.reverse_url('rooms', group_id))


class RoomSocketHandler(tornado.websocket.WebSocketHandler):
    from .rooms import Rooms
    from .cards import Cards
    from .chat import Chat
    rooms = Rooms()
    cards = Cards()
    chat = Chat()

    def open(self, *args, **kwargs):
        print('WebSocket Opened')

    def on_message(self, message):
        print('WebSocket Received')
        print(json.loads(message))
        message = json.loads(message)
        if message['action'] == 'initializeMe':
            self.initClient()
        elif message['action'] == 'joinRoom':
            self.joinRoom(message)
        elif message['action'] == 'moveCard':
            self.move_card(message)
        elif message['action'] == 'createCard':
            self.create_card(message)
        elif message['action'] == 'editCard':
            self.edit_card(message)
        elif message['action'] == 'deleteCard':
            self.delete_card(message)
        elif message['action'] == 'changeTheme':
            self.change_theme(message)
        elif message['action'] == 'voteUp':
            self.vote_up(message)
        elif message['action'] == 'chat':
            self.update_chat(message)

    def on_close(self):
        print('WebSocket Closed')
        self.rooms.remove_client(self)

    def joinRoom(self, message):
        self.rooms.add_to_room(self, message['data'])
        print("Message")
        print(message['data'])
        self.write_message(json.dumps({'action': 'roomAccept', 'data': ''}))

    def roundRand(self, value):
        return random.randint(0, value)

    def initClient(self):
        room_id = self.rooms.get_room_id(self)
        print('user has entered the room {0}'.format(room_id))

        user = BaseHandler.get_current_user(self)

        if not self.rooms.checks_user_already_in_room_of(room_id, user["name"]):
            self.rooms.add_user(room_id, user["name"])
            self.chat.set_nickname(room_id, user["name"])

        nickname = self.chat.get_nickname(room_id, user["name"])

        self.write_message(json.dumps({'action': 'initCards', 'data': self.cards.get_all(room_id)}))
        self.write_message(json.dumps({'action': 'initColumns', 'data': ''}))
        self.write_message(json.dumps({'action': 'changeTheme', 'data': 'bigcards'}))
        self.write_message(json.dumps({'action': 'setBoardSize', 'data': ''}))
        self.write_message(json.dumps({'action': 'initialUsers', 'data': ''}))
        self.write_message(json.dumps({'action': 'chatMessages', 'data': {'cache': self.chat.cache[room_id],
                                                                          'name': nickname}}))

    def move_card(self, message):
        message_out = {
            'action': message['action'],
            'data': {
                'id': message['data']['id'],
                'position': {
                    'left': message['data']['position']['left'],
                    'top': message['data']['position']['top'],
                }
            }
        }
        self.broadcast_to_room(self, message_out)
        room_id = self.rooms.get_room_id(self)
        self.cards.update_xy(room_id, card_id=message['data']['id'], x=message['data']['position']['left'], y=message['data']['position']['top'])

    def create_card(self, message):
        data = message['data']
        clean_data = {'text': data['text'], 'id': data['id'], 'x': data['x'], 'y': data['y'],
                      'rot': data['rot'], 'colour': data['colour'], 'sticker': None, 'vote_count': 0}
        message_out = {
            'action': 'createCard',
            'data': clean_data
        }
        self.broadcast_to_room(self, message_out)
        room_id = self.rooms.get_room_id(self)
        self.cards.add(room_id, clean_data)

    @asynchronous
    @gen.engine
    def edit_card(self, message):
        id = message['data']['id']
        text = message['data']['value']
        clean_data = {'value': text, 'id': id}
        message_out = {
            'action': 'editCard',
            'data': clean_data
        }
        self.broadcast_to_room(self, message_out)
        room_id = self.rooms.get_room_id(self)
        self.cards.update_text(room_id, card_id=id, text=text)
        from handlers.agent.sentence_generator import SentenceGenerator
        sentence_generator = SentenceGenerator()
        res = sentence_generator.generate_sentence(text)
        for sent in res:
            message_out = {'action': 'advice', 'data': {'sent': sent}}
            self.write_message(json.dumps(message_out))
            yield gen.sleep(2.5)

    def delete_card(self, message):
        clean_message = {
            'action': 'deleteCard',
            'data': {'id': message['data']['id']}
        }
        self.broadcast_to_room(self, clean_message)
        room_id = self.rooms.get_room_id(self)
        self.cards.delete(room_id, card_id=message['data']['id'])

    def change_theme(self, message):
        clean_message = {'data': message['data'], 'action': 'changeTheme'}
        self.broadcast_to_room(self, clean_message)

    def vote_up(self, message):
        print("vote-1up")
        # notify vote_count
        # update vote_count
        clean_message = {
            'action': 'voteUp',
            'data': {'id': message['data']['id']}
        }
        self.broadcast_to_room(self, clean_message)
        room_id = self.rooms.get_room_id(self)
        self.cards.update_vote_count(room_id, card_id=message['data']['id'])

    def update_chat(self, message):
        room_id = self.rooms.get_room_id(self)

        print("update_chat")

        chat_data = {'id': str(uuid.uuid4()),
                     'body': message['data']["body"],
                     'name': message['data']['name']
        }
        self.chat.update_cache(chat_data, room_id)
        print(message['data']['name'])
        message_out = {
            'data': chat_data, 'action': 'chat'
        }
        self.broadcast_to_room(self, message_out)

    def broadcast_to_room(self, client, message_out):
        room_id = self.rooms.get_room_id(client)
        for waiter in self.rooms.get_room_clients(room_id):
            print("waiter")
            print(waiter)
            if waiter == client:
                continue
            waiter.write_message(json.dumps(message_out))
