# -*- coding: utf-8 -*-
from collections import defaultdict

class Rooms(object):
    rooms = defaultdict(set)  # rooms[room_id].add(clientsock)
    clients = {}

    def __init__(self):
        """
        self.user_on_rooms = {
            room_id1: set(client_name),
            room_id2: set(),
            ...
            room_idn: set()
        }
        """
        self.users_in_rooms = defaultdict(set)

    def count_user_already_in_room_of(self, room_id):
        return len(self.rooms[room_id])

    def checks_user_already_in_room_of(self, room_id, client_name):
        return client_name in self.users_in_rooms[room_id]

    def add_user(self, room_id, client_name):
        self.users_in_rooms[room_id].add(client_name)

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
        print("-----------------------")
        print(self.rooms[room_id])
        self.rooms[room_id] -= set([client])
        print(self.rooms[room_id])

    def clear_users_in_room(self, room_id):
        del self.users_in_rooms[room_id]
