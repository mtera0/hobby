# dj_spotify
## 1.プロジェクト概要
spotifyの既存のプレイリストを利用して、DJが再生するような順番に並べ替えたプレイリストを作成。
BPM, key, 雰囲気のいずれかが近いトラック同士を隣り合わせることでDJらしさを再現できると考えた。

## 2.主要技術

| 言語・モジュール | バージョン |
| -------------------- | ---------- |
| Python                | 3.9.12       |
| pandas                | 1.5.3       |
| spotipy                | 2.24.0       |
| python-dotenv                | 1.0.1       |

## 3.開発環境構築方法

#### 1. Python のインストール

Python をインストール。インストール方法は[公式ドキュメント](https://www.python.org/downloads/)を参照。

#### 2. pandas, spotipy, python-dotenvのインストール

[pandas](https://pandas.pydata.org/docs/getting_started/install.html), [python-dotenv](https://pypi.org/project/python-dotenv/), [spotipy](https://pypi.org/project/spotipy/) のうちインストールしていないものがあれば以下のコマンドによりインストール。詳細の確認はそれぞれのリンクより可能。

```
pip install pandas

pip install python-dotenv

pip install spotipy
```

#### 3. 環境変数の設定
実行時に必要な情報を.envファイルにて設定。環境変数の一覧は以下の通り。

| 変数名                 | 概要                                      |
| ---------------------- | ----------------------------------------- |
| CLIENT_ID    | spotifyのclient_id　 |
| CLIENT_SECRET         | spotifyのclient_secret   |
| USER_NAME             | spotifyのユーザ名         |
| PLAYLIST_ID         | 利用するプレイリストID       |
| PLAYLIST_NAME         | 利用するプレイリスト名       |

それぞれの変数の確認方法は次のようになっている。
###### CLIENT_ID, CLIENT_SECRET
1. [spotify開発者のダッシュボード](https://developer.spotify.com/dashboard)のcreat appからアプリを作成
2. アプリのsettings画面からClient IDとClient secretを取得

###### USER_NAME
1. spotifyのホーム画面から画面右上のアカウントボタンによりアカウント画面へ遷移
2. プロフィールを編集 の画面のユーザー名の下に記載されているアルファベットと数字の記号列をUSER_NAMEとして取得

###### PLAYLIST_ID, PLAYLIST_NAME
1. 利用するプレイリストを選択
2. PLAYLIST_IDはURLのうち " https://open.spotify.com/playlist/ "以降の部分、PLAYLIST_NAMEは画面に表示されているものを取得
