# -*- coding: utf-8 -*-
import random
from collections import defaultdict

class Chat(object):

    cache_size = 200
    user_num = list(range(1, 100))
    random.shuffle(user_num)

    def __init__(self):
        """
        self.user_on_rooms = {
            room_id1: set( client_name),
            room_id2: set(),
            ...
            room_idn: set()
        }
        """
        self.cache = defaultdict(list)
        self.nickname_dic = defaultdict(list)
        self.users_in_rooms = defaultdict(set)

    def checks_user_already_in_room_of(self, room_id, client_name):
        return client_name in self.users_in_rooms[room_id]

    def add_user(self, room_id, client_name):
        self.users_in_rooms[room_id].add(client_name)
        print("add user in ")
        print(self.users_in_rooms)
        print(self.users_in_rooms[room_id])
        self.__set_nickname(room_id, client_name)

    def __set_nickname(self, room_id, client_name):
        self.nickname_dic[room_id] = {client_name: 'user' + str(self.__get_random_name())}

    def get_nickname(self, room_id, client_name):
        return self.nickname_dic[room_id][client_name]

    def update_cache(self, chat, room_id):
        self.cache[room_id].append(chat)
        if len(self.cache[room_id]) > self.cache_size:
            self.cache[room_id] = self.cache[-self.cache_size:]

    def __get_random_name(self):
        return self.user_num.pop()
