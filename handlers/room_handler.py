import tornado.websocket
from .base_handler import BaseHandler


class RoomsHandler(BaseHandler):
    pass


class RoomHandler(BaseHandler):
    pass


class RoomSocketHandler(tornado.websocket.WebSocketHandler):
    pass