# -*- coding: utf-8 -*-
# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='cp932')
import random
from .keyword_extraction import YahooKeyphraseExtraction
from .named_entity_extraction import DocomoNamedEntityExtraction
from .praise import praises, proposals, available_answer
import asyncio

class SentenceGenerator(object):

    def __init__(self):
        self.keyphrase_extractor = YahooKeyphraseExtraction()
        self.named_entity_extractor = DocomoNamedEntityExtraction()
    @asyncio.coroutine
    def generate_sentence(self, text):
        keyphrase_dic = self.keyphrase_extractor.search(text)
        if not keyphrase_dic or 'Error' in keyphrase_dic:
            return []
        named_entity_list = self.named_entity_extractor.search(text)
        if not named_entity_list:
            word = self.select_word_with_max_score(keyphrase_dic)
            return [self.generate_praise(word)]
        word = self.select_word_with_max_score(keyphrase_dic)
        if not self.get_named_entity(word, named_entity_list):
            return []
        named_entity = self.get_named_entity(word, named_entity_list)
        res = []
        res.append(self.generate_praise(word))
        res.append(self.generate_proposal(word, named_entity))
        return res

    def get_named_entity(self, word, named_entity_list):
        for w, ne in named_entity_list:
            if w == word:
                return ne
        return None

    def select_word_with_max_score(self, keyphrase_dic):
        keyphrase_list = sorted(keyphrase_dic.items(), key=lambda x:x[1])
        return keyphrase_list[-1][0]

    def generate_praise(self, word):
        praise = random.choice(praises)
        return praise.format(word)

    def generate_proposal(self, word, named_entity):
        available_answer_list = available_answer[named_entity]
        answer_id = random.choice(available_answer_list)
        return proposals[answer_id].format(word)

if __name__ == '__main__':
    # 文を与えると、褒める文と発想の転換を促す文を生成する
    text = u"東京ミッドタウンから国立新美術館まで歩いて5分で着きます。"
    # text = '誰でもアイディアを簡単に出せるホワイトボード'
    print('入力：')
    print(' ' + text)
    sentence_generator = SentenceGenerator()
    res = sentence_generator.generate_sentence(text)
    print('出力：')
    for sent in res:
        print('　' + sent)