# pydomino-docker
音素アラインメントツール`pydomino`をdocker上で利用できるようにしました  
pydominoは入力に`音素テキスト`が必要ですが、OpenJTalkを利用することによって`かなテキスト`も入力可能になっています  

## 準備
1. 音素アラインメントを行いたいWAVファイルをwavディレクトリに配置します
1. pydomino-dockerディレクトリ内に音素テキストの場合はphoneme.txt、かなテキストの場合はkana.txtを作成しテキストを記入します

テキストはWAVファイル1つにつき1行で入力します  
テキスト行の並び順は、WAVファイルをファイル名で昇順ソートしたときと同じにしてください  
WAVファイルの数とテキストの行数は一致している必要があります  

音素テキストの場合は以下のリンク先を参考に、音素を半角スペースで区切って入力します  
参考: https://github.com/DwangoMediaVillage/pydomino  

かなテキストの場合は`ひらがな`または`カタカナ`で入力します  

## アラインメント
以下のコマンドを実行します  
```
$ docker compose build
$ docker compose run app bash
$ python3 phoneme.py  // 音素テキスト入力の場合
$ python3 kana.py     // かなテキスト入力の場合
$ exit
$ docker compose down
```

## 音素変換について
OpenJTalkでkana.txtから変換された音素は、pydominoで使用される音素と一部異なります  
そのため、以下のように分割または変換されます  
- ty -> t, y
- gw -> g, w
- kw -> k, w
- sil -> pau

## ライセンス
Copyright (c) 2024 KoharuYuzuki  
MIT License (https://opensource.org/license/mit/)  
