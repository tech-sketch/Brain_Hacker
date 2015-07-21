# -*- coding: utf-8 -*-
import random
import itertools
from collections import defaultdict


class Chat(object):

    cache_size = 200
    # user_num = list(range(1, 100))
    # random.shuffle(user_num)
    colors = ['赤', '青', '黄', '緑', '紫', '黒', '茶', '灰色', '金', '銀']
    fruits = ['りんご', 'みかん', 'メロン', 'パイナップル', 'ぶどう', '梨', 'いちご', 'もも', 'さくらんぼ', 'バナナ']
    fruits_with_color = itertools.product(colors, fruits)
    user_name = list(map(lambda n: n[0]+n[1], fruits_with_color))
    random.shuffle(user_name)

    def __init__(self):
        self.cache = defaultdict(list)
        self.nickname_dic = defaultdict(dict)

    def set_nickname(self, room_id, client_name):
        self.nickname_dic[room_id].update({client_name:str(self.__get_random_name())})

    def get_nickname(self, room_id, client_name):
        return self.nickname_dic[room_id][client_name]

    def update_cache(self, chat, room_id):
        self.cache[room_id].append(chat)
        if len(self.cache[room_id]) > self.cache_size:
            self.cache[room_id] = self.cache[-self.cache_size:]

    def __get_random_name(self):
        return self.user_name.pop()

    def clear_caches(self, room_id):
        del self.cache[room_id]
        del self.nickname_dic[room_id]
