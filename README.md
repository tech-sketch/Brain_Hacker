# Brain	Hacker
Brain Hackerは、Web上でブレインストーミングをするためのアプリケーションです。
匿名でブレインストーミングを行うことができるので、相手を気にせず、自由に意見を出すことができます。
また、褒める機能と思考支援機能を持つAIを搭載することで、楽しく、創造的なブレインストーミングを可能にします。

## インストール方法

### 動作環境
**プラットフォーム:** 以下のプラットフォームでの動作は確認しています。
* Linux(Ubuntu 14.04)
* Windows 7

**データベース:** データベースは、標準ではPostgreSQLを想定しています。以下のバージョンでの動作は確認しています。
* PostgreSQL 9.4
また、Brain_Hacker/settings.pyで使用するデータベースの設定を行うことで、MySQLなどにも対応することができます。


### モジュールのインストール
Brain Hackerを動作させるために必要なモジュールは以下のコマンドでインストールできます。
```shell
$ pip install -r requirements.txt
```

### 外部APIキーの設定
思考支援機能を使うためには、以下の2つのAPIキーが必要になります。
* [Yahoo キーフレーズ抽出](http://developer.yahoo.co.jp/webapi/jlp/keyphrase/v1/extract.html)
* [Docomo 固有表現抽出](https://dev.smt.docomo.ne.jp/?p=docs.api.page&api_name=language_analysis&p_name=api_2#tag01)

APIキーはそれぞれ、
* handlers/agent/keyword_extraction.py
* handlers/agent/named_entity_extraction.py
の中の、keyidに記述してください。


## 実行方法
実行方法では、データベースの設定、ポートの設定、アプリケーションの実行方法について説明します。
### データベースの設定
Brain_Hacker/settings.pyで、データベースの設定を行います。以下はPostgreSQLにおける設定例です。
```python
DATABASES = {
    'default': {
        'ENGINE': 'postgresql+psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '*****',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

設定が終わったら、以下のコマンドを実行して、データベースにテーブルを作成します。
```shell
$ cd models
$ python user.py
$ python group.py
$ python room.py
```


### ポートの設定
Brain_Hacker/settings.pyで、アプリケーションを動作させるポートの設定を行います。以下が設定例です。
```python
define('port', default=8888, help="run on the given port", type=int)
```
設定例では、デフォルトのポート番号を8888にしています。それ以外にも、ポート番号は実行時に指定することもできます。

### アプリケーションの実行
アプリケーションは以下のコマンドで実行します。
```shell
$ python app.py
```
また、実行時にポート番号を指定することで、指定したポート番号でアプリケーションを実行することができます。以下では、ポート番号に8000番を指定して実行しています。
```shell
$ python app.py --port=8000
```
アプリケーションをポート番号8888番で起動後、ブラウザでhttp://127.0.0.1:8888/にアクセスしてトップページが表示されることを確認します。