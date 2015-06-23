# -*- coding: utf-8 -*-
from collections import defaultdict

class Rooms(object):
    rooms = defaultdict(set)  # rooms[room_id].add(clientsock)
    clients = {}

    def add_to_room(self, client, room_id):
        self.rooms[room_id].add(client)
        self.clients[client] = room_id

    def get_room_clients(self, room_id):
        return self.rooms[room_id]

    def get_room_id(self, client):
        return self.clients[client]

    def remove_client(self, client):
        room_id = self.clients[client]
        del self.clients[client]
        self.rooms[room_id] -= set([client])
