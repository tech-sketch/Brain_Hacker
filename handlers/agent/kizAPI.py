# -*- coding: utf-8 -*-
from urllib.parse import urlencode
from urllib.request import urlopen
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='cp932')


if __name__ == '__main__':
    url = 'http://kizasi.jp/kizapi.py?span=24&{0}&type=coll'
    params = {
        'kw_expr': '通勤時間',
    }
    full_url = url.format(urlencode(params))
    res = urlopen(full_url).read().decode('utf-8')
    import re
    p = re.compile(r'<title>.*?</title>')
    similar_words = [word.lstrip('<title>').rstrip('</title>') for word in p.findall(res)]
    for w in similar_words:
        print(w)