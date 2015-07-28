# -*- coding:utf8 -*-
from urllib.parse import urlencode
from urllib.request import urlopen
import json
# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='cp932')


class YahooKeyphraseExtraction(object):

    def __init__(self):
        self.__keyid = ''
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

import tornado.web
import tornado.gen
import tornado.httpclient
class KeyphraseExtraction(object):
    def __init__(self):
        self.__keyid = ''
        self.__url = 'http://jlp.yahooapis.jp/KeyphraseService/V1/extract'

    @tornado.web.asynchronous
    @tornado.gen.engine
    def search(self, text):
        request_url = self.__url + '?{0}'.format(urlencode({'appid': self.__keyid, 'sentence': text, 'output': 'json'}))
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(client.fetch, request_url)
        body = json.loads(response.body)
        return body

'''
def handle_request(response):
    if response.error:
        print("Error:", response.error)
    else:
        print(response.body)
from tornado.httpclient import AsyncHTTPClient
http_client = AsyncHTTPClient()
http_client.fetch("http://www.google.com/", handle_request)
'''
if __name__ == '__main__':
    text = u"東京ミッドタウンから国立新美術館まで歩いて5分で着きます。"
    api = KeyphraseExtraction()
    result = api.search(text)
    print(result)
    #for k, v in result.items():
     #   print(k, v)
