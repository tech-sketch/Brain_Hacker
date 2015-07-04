# Brain	Hacker
Brain Hackerは、Web上でブレインストーミングをするためのアプリケーションです。
匿名でブレインストーミングを行うことができるので、相手を気にせず、自由に意見を出すことができます。
また、褒める機能と思考支援機能を持つAIを搭載することで、楽しく、創造的なブレインストーミングを可能にします。

## インストール方法
```shell
$ pip install -r requirements.txt
```

**必要条件:** Python3系のインストールは必須です。
また、思考支援機能を使うためには、以下の2つのAPIキーが必要になります。
* [Yahoo キーフレーズ抽出](http://developer.yahoo.co.jp/webapi/jlp/keyphrase/v1/extract.html)
* [Docomo 固有表現抽出](https://dev.smt.docomo.ne.jp/?p=docs.api.page&api_name=language_analysis&p_name=api_2#tag01)

**プラットフォーム:** 以下のプラットフォームでの動作は確認しています。
* Linux(Ubuntu?)
* Windows7

## 実行方法
```shell
$ python app.py
```

## Readmeに書く内容
* サービスの概要
* サービスの使い方
* インストール方法、実行方法
* 動作に必要な環境


* 既知の不具合、今後実装すべき機能がIssueに洗い出されていること
* Readmeに書けない（書くべきでない）細かい仕様や実行手順はGithubのWikiに記載。

## 参考
* https://github.com/tornadoweb/tornado
