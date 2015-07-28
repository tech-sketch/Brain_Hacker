import uuid

import tornado.web
import tornado.websocket
from tornado import gen
from tornado.web import asynchronous
from tornado.escape import json_encode, json_decode, xhtml_unescape, xhtml_escape

from handlers.base_handler import BaseHandler
from models.room import Room
from models.group import Group
from models.user import User
from models.idea import Idea
from .util import check_group_permission
from forms.forms import RoomForm
from handlers.brainstorming.rooms import Rooms
from handlers.brainstorming.cards import Cards
from handlers.brainstorming.chat import Chat
from handlers.agent.sentence_generator import SentenceGenerator


class RoomsHandler(BaseHandler):

    @check_group_permission
    @tornado.web.authenticated
    def get(self, group_id):
        room_name = self.get_argument('room_name', '')
        rooms = Room.search_name(room_name)
        rooms = [room for room in rooms if room.belongs_to_group(group_id)]
        self.render('room/rooms.html', rooms=rooms, group_id=group_id)

    @check_group_permission
    @tornado.web.authenticated
    def post(self, group_id):
        form = RoomForm(self.request.arguments)
        if form.validate():
            room = Room(**form.data)
            group = Group.get(group_id)
            group.rooms.append(room)
            group.save()
        self.redirect(self.reverse_url('rooms', group_id))


class RoomHandler(BaseHandler):

    @check_group_permission
    @tornado.web.authenticated
    def get(self, group_id, room_id):
        room = Room.get(room_id)
        self.render('room/brainstorming.html', room=room)
        #self.render('room/room.html', room=room)


class RoomEditHandler(BaseHandler):

    @check_group_permission
    @tornado.web.authenticated
    def post(self, group_id, room_id):
        form = RoomForm(self.request.arguments)
        if form.validate():
            room = Room.get(room_id)
            room.update(**form.data)
            room.save()
        self.redirect(self.reverse_url('rooms', group_id))


class RoomDeleteHandler(BaseHandler):

    @check_group_permission
    @tornado.web.authenticated
    def post(self, group_id, room_id):
        Room.get(room_id).delete()
        self.redirect(self.reverse_url('rooms', group_id))

from handlers.base_handler import BaseHandler


class BaseSocketHandler(BaseHandler, tornado.websocket.WebSocketHandler):
    pass


class RoomSocketHandler(BaseSocketHandler):
    rooms = Rooms()
    cards = Cards()
    chat = Chat()

    def open(self, *args, **kwargs):
        print('neko')
        pass

    def on_message(self, message):
        message = json_decode(message)
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
            pass
        elif message['action'] == 'voteUp':
            self.vote_up(message)
        elif message['action'] == 'chat':
            self.update_chat(message)

    def on_close(self):
        room_id = self.rooms.get_room_id(self)
        self.broadcast_to_room(self, self.generate_message('countUser',
                                                           self.rooms.count_user_already_in_room_of(room_id) - 1))
        self.rooms.remove_client(self)

        clients_name = self.rooms.get_room_clients_name(room_id)
        message_out = self.generate_message('getMember', ", ".join(clients_name))
        for waiter in self.rooms.get_room_clients(room_id):
            waiter.send_message(message_out)

    def joinRoom(self, message):
        self.rooms.add_to_room(self, message['data'])
        message_out = self.generate_message(action='roomAccept', data='')
        self.send_message(message_out)

        room_id = self.rooms.get_room_id(self)
        user = BaseHandler.get_current_user(self)
        self.broadcast_to_all_room_user(self, self.generate_message('countUser',
                                                                    self.rooms.count_user_already_in_room_of(room_id)))

        clients_name = self.rooms.get_room_clients_name(room_id)
        message_out = self.generate_message('getMember', ", ".join(clients_name))
        self.broadcast_to_all_room_user(self, message_out)

    def initClient(self):
        room_id = self.rooms.get_room_id(self)
        user = BaseHandler.get_current_user(self)

        if not self.rooms.checks_user_already_in_room_of(room_id, user["name"]):
            self.rooms.add_user(room_id, user["name"])
            self.chat.set_nickname(room_id, user["name"])

        nickname = self.chat.get_nickname(room_id, user["name"])

        self.send_message(self.generate_message('initCards', self.cards.get_all(room_id)))
        self.send_message(self.generate_message('changeTheme', 'bigcards'))
        self.send_message(self.generate_message('chatMessages', {'cache': self.chat.cache[room_id], 'name': nickname}))

    def move_card(self, message):
        self.broadcast_to_room(self, message)
        room_id = self.rooms.get_room_id(self)
        self.cards.update_xy(room_id, card_id=message['data']['id'],
                             x=message['data']['position']['left'], y=message['data']['position']['top'])

    def create_card(self, message):
        message_out = self.generate_message('createCard', message['data'])
        self.broadcast_to_room(self, message_out)
        room_id = self.rooms.get_room_id(self)
        self.cards.add(room_id, message['data'])

        # --
        idea = Idea(card_id=message['data']['id'])
        idea.save()

    @asynchronous
    @gen.engine
    def edit_card(self, message):
        id = message['data']['id']
        text = xhtml_unescape(message['data']['value'].strip())
        clean_data = {'value': text, 'id': id}

        message_out = self.generate_message('editCard', clean_data)
        self.broadcast_to_all_room_user(self, message_out)
        room_id = self.rooms.get_room_id(self)
        self.cards.update_text(room_id, card_id=id, text=xhtml_escape(text))

        sentence_generator = SentenceGenerator()
        res = sentence_generator.generate_sentence(text)
        for sent in res:
            message_out = self.generate_message('advice', {'sent': sent})
            self.send_message(message_out)
            yield gen.sleep(2.5)

    def delete_card(self, message):
        self.broadcast_to_room(self, message)
        room_id = self.rooms.get_room_id(self)
        self.cards.delete(room_id, card_id=message['data']['id'])

    def change_theme(self, message):
        pass  # self.broadcast_to_room(self, message)

    def vote_up(self, message):
        message_id = message['data']['id']
        user = User.get(BaseHandler.get_current_user_id(self))
        idea = Idea.get_from_cardID(card_id=message_id)

        if idea not in user.ideas:
            user.ideas.append(idea)
            user.save()

            message_out = self.generate_message('voteUp', {'id': message_id})
            self.broadcast_to_room(self, message_out)
            room_id = self.rooms.get_room_id(self)
            self.cards.update_vote_count(room_id, card_id=message_id)
        else:
            message_out = self.generate_message('voteDown', {'id': message_id})
            self.send_message(message_out)

    def update_chat(self, message):
        room_id = self.rooms.get_room_id(self)
        chat_data = {'id': str(uuid.uuid4()),
                     'body': message['data']["body"],
                     'name': message['data']['name']
                     }
        self.chat.update_cache(chat_data, room_id)

        message_out = self.generate_message('chat', chat_data)
        self.broadcast_to_room(self, message_out)

    def broadcast_to_room(self, client, message_out):
        room_id = self.rooms.get_room_id(client)
        for waiter in self.rooms.get_room_clients(room_id):
            if waiter == client:
                continue
            waiter.send_message(message_out)

    def broadcast_to_all_room_user(self, client, message_out):
        room_id = self.rooms.get_room_id(client)
        for waiter in self.rooms.get_room_clients(room_id):
            waiter.send_message(message_out)

    def send_message(self, message):
        self.write_message(json_encode(message))

    def generate_message(self, action, data):
        return {'action': action, 'data': data}
































class BrainstormingHandler(BaseSocketHandler):
    rooms = Rooms()
    cards = Cards()
    chat = Chat()

    def open(self, *args, **kwargs):
        pass

    def on_message(self, message):
        message = json_decode(message)
        print(message)
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
        elif message['action'] == 'voteUp':
            self.vote_up(message)
        elif message['action'] == 'chat':
            self.update_chat(message)

    def on_close(self):
        room_id = self.rooms.get_room_id(self)
        self.broadcast_to_room(self, self.generate_message('countUser',
                                                           self.rooms.count_user_already_in_room_of(room_id) - 1))
        self.rooms.remove_client(self)

        clients_name = self.rooms.get_room_clients_name(room_id)
        message_out = self.generate_message('getMember', clients_name)
        for waiter in self.rooms.get_room_clients(room_id):
            waiter.send_message(message_out)

    def joinRoom(self, message):
        self.rooms.add_to_room(self, message['data'])
        message_out = self.generate_message(action='roomAccept', data='')
        self.send_message(message_out)

        room_id = self.rooms.get_room_id(self)
        user = BaseHandler.get_current_user(self)
        self.broadcast(self.generate_message('countUser', self.rooms.count_user_already_in_room_of(room_id)))

        clients_name = self.rooms.get_room_clients_name(room_id)
        message_out = self.generate_message('getMember', clients_name)
        self.broadcast(message_out)

    def initClient(self):
        room_id = self.rooms.get_room_id(self)
        user = BaseHandler.get_current_user(self)

        if not self.rooms.checks_user_already_in_room_of(room_id, user["name"]):
            self.rooms.add_user(room_id, user["name"])
            self.chat.set_nickname(room_id, user["name"])

        nickname = self.chat.get_nickname(room_id, user["name"])

        self.send_message(self.generate_message('initCards', self.cards.get_all(room_id)))
        self.send_message(self.generate_message('chatMessages', {'cache': self.chat.cache[room_id], 'name': nickname}))

    def move_card(self, message):
        self.broadcast_to_room(self, message)
        room_id = self.rooms.get_room_id(self)
        self.cards.update_xy(room_id, card_id=message['data']['id'],
                             x=message['data']['position']['left'], y=message['data']['position']['top'])

    @asynchronous
    @gen.engine
    def create_card(self, message):
        message_out = self.generate_message('createCard', message['data'])
        self.broadcast(message_out)
        room_id = self.rooms.get_room_id(self)
        self.cards.add(room_id, message['data'])

        idea = Idea(card_id=message['data']['id'])
        idea.save()

        # sentence_generator = SentenceGenerator()
        # res = sentence_generator.generate_sentence(message['data']['text'])
        # for sent in res:
        #     message_out = self.generate_message('advice', {'sent': sent})
        #     self.send_message(message_out)
        #     yield gen.sleep(2.5)

    def edit_card(self, message):
        id = message['data']['id']
        text = xhtml_unescape(message['data']['value'].strip())
        clean_data = {'value': text, 'id': id}

        message_out = self.generate_message('editCard', clean_data)
        self.broadcast(message_out)
        room_id = self.rooms.get_room_id(self)
        self.cards.update_text(room_id, card_id=id, text=xhtml_escape(text))

    def delete_card(self, message):
        self.broadcast_to_room(self, message)
        room_id = self.rooms.get_room_id(self)
        self.cards.delete(room_id, card_id=message['data']['id'])

    def vote_up(self, message):
        message_id = message['data']['id']
        thumb_up_count = message['data']['thumb-up-count']
        user = User.get(BaseHandler.get_current_user_id(self))
        idea = Idea.get_from_cardID(card_id=message_id)
        if idea not in user.ideas:
            user.ideas.append(idea)
            user.save()

            message_out = self.generate_message('voteUp', {'id': message_id, 'thumb-up-count': thumb_up_count + 1})
            self.broadcast(message_out)
            room_id = self.rooms.get_room_id(self)
            self.cards.update_vote_count(room_id, card_id=message_id)

    def update_chat(self, message):
        room_id = self.rooms.get_room_id(self)
        chat_data = {'id': str(uuid.uuid4()),
                     'body': message['data']["body"],
                     'name': message['data']['name']
                     }
        self.chat.update_cache(chat_data, room_id)

        message_out = self.generate_message('chat', chat_data)
        self.broadcast(message_out)

    def broadcast_to_room(self, client, message_out):
        room_id = self.rooms.get_room_id(client)
        for waiter in self.rooms.get_room_clients(room_id):
            if waiter == client:
                continue
            waiter.send_message(message_out)

    def broadcast_to_all_room_user(self, client, message_out):
        room_id = self.rooms.get_room_id(client)
        for waiter in self.rooms.get_room_clients(room_id):
            waiter.send_message(message_out)

    def broadcast(self, message):
        room_id = self.rooms.get_room_id(self)
        for waiter in self.rooms.get_room_clients(room_id):
            waiter.send_message(message)

    def send_message(self, message):
        self.write_message(json_encode(message))

    def generate_message(self, action, data):
        return {'action': action, 'data': data}
