import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import config
from utils import get_dj_track_id_list, make_dj_playlist
import sys


# spotifyへの認証。プレイリストの読み込みと書き込みに関するscopeを選択している。
scope = 'playlist-read-collaborative playlist-read-private playlist-modify-private playlist-modify-public'
token = spotipy.util.prompt_for_user_token(config.USER_NAME, scope, config.CLIENT_ID, config.CLIENT_SECRET,redirect_uri='http://example.com')

sp = spotipy.Spotify(auth=token)

# 既存のプレイリストを取得
result = sp.user_playlist(config.USER_NAME, config.PLAYLIST_ID)

# プレイリストをDJ風に並び替えたトラックのidのリストを作成
df_dj = get_dj_track_id_list(sp, result)

# idのリストをもとに新規のプレイリストを作成
make_dj_playlist(sp, df_dj)


