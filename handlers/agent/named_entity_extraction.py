# -*- coding: utf-8 -*-
from urllib.parse import urlencode
from urllib.request import urlopen
import json
# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='cp932')

class DocomoNamedEntityExtraction(object):

    def __init__(self):
        self.__keyid = ''
        self.__url = 'https://api.apigw.smt.docomo.ne.jp/gooLanguageAnalysis/v1/entity?APIKEY=' + self.__keyid

    def search(self, text):
        params = {
            'sentence': text,
        }
        data = urlencode(params).encode('utf-8')
        with urlopen(self.__url, data) as page:
            byte_json_data = page.read()
        json_data = byte_json_data.decode('utf-8')
        result = json.loads(json_data)
        return result['ne_list']

if __name__ == '__main__':
    text = u"東京ミッドタウンから国立新美術館まで歩いて5分で着きます。"
    api = DocomoNamedEntityExtraction()
    result = api.search(text)
    print(result)
    for k, v in result.items():
        print(k, v)
