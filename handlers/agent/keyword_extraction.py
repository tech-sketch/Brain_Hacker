# -*- coding:utf8 -*-
from urllib.parse import urlencode
from urllib.request import urlopen
import json
# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='cp932')


class YahooKeyphraseExtraction(object):

    def __init__(self):
        self.__keyid = 'dj0zaiZpPWtLOThUbTE1ak5kYyZzPWNvbnN1bWVyc2VjcmV0Jng9YWM-'
        self.__url = 'http://jlp.yahooapis.jp/KeyphraseService/V1/extract'

    def search(self, text):
        params = {
            'appid': self.__keyid,
            'sentence': text,
            'output': 'json',
        }
        full_url = self.__url + '?{0}'.format(urlencode(params))
        try:
            with urlopen(full_url) as page:
                byte_json_data = page.read()
        except:
            print("Keyword Extraction Error")
            return {}
        json_data = byte_json_data.decode('utf-8')
        return json.loads(json_data)

if __name__ == '__main__':
    text = u"東京ミッドタウンから国立新美術館まで歩いて5分で着きます。"
    api = YahooKeyphraseExtraction()
    result = api.search(text)
    print(result)
    for k, v in result.items():
        print(k, v)
