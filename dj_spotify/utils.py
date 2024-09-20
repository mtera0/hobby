import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import pandas as pd
import sys

import config



def get_track_data(sp, result):
  '''
  colをBPM,key,moodに関する情報, rawを各トラックのデータとしたdataframeを作成
  1. columnsのみが渡された空のdataframeを準備
  2. id_listのidから各トラックのBPM,key,moodに関する情報を取得。moodはacousticness,danceability,loudness,energyの近さで決定
  3. 取得したトラックの情報をdataframeに連結
  '''
  features = []
  cnt = 0
  df = pd.DataFrame(columns=['BPM','key','acousticness','danceability','loudness','energy'])

  for track in result['tracks']['items']:
    # プレイリスト内の曲のidごとにデータを抜き出してdataframe化
    id = track['track']['id']
    feature = sp.audio_features(id)[0]
    tempo = feature['tempo']
    key = feature['key']
    acousticness = feature['acousticness']
    danceability = feature['danceability']
    loudness = feature['loudness']
    energy = feature['energy']
    df.loc[id] = [tempo, key, acousticness, danceability, loudness, energy]
  
  return df


def get_next_dj_data(df, df_dj, priority_list):
  '''
  df_djの最後のトラックに繋がるトラックを取得。
  priority_list=['BPM','key','mood']でindexの小さいものほど優先度が高いとする。
  '''
  check = False
  for i_priority in priority_list:
    
    if i_priority == 'BPM':
      for idx, row in df.iterrows():
        if  (row['BPM']-5) <= df_dj.tail(1)['BPM'][0] <= (row['BPM']+5):
          df_dj.loc[idx] = row
          df = df.drop(index=idx, inplace=False)
          check = True
          break
      if check == True:
        break

    elif i_priority == 'key':
      for idx, row in df.iterrows():
        if  (row['key']-1) <= df_dj.tail(1)['key'][0]  <= (row['key']+1):
          df_dj.loc[idx] = row
          df = df.drop(index=idx, inplace=False)
          check = True
          break
      if check == True:
        break

    else:
      for idx, row in df.iterrows():
        if  (((row['acousticness']-0.2) <= df_dj.tail(1)['acousticness'][0] <= (row['acousticness']+0.2))) &\
            (((row['danceability']-0.1) <= df_dj.tail(1)['danceability'][0] <= (row['danceability']+0.1))) &\
            (((row['loudness']-1) <= df_dj.tail(1)['loudness'][0] <= (row['loudness']+1))) &\
            (((row['energy']-0.1) <= df_dj.tail(1)['energy'][0] <= (row['energy']+0.1))):
          df_dj.loc[idx] = row
          df = df.drop(index=idx, inplace=False)
          check = True
          break
      if check == True:
        break
    
  return df, df_dj, check


def get_dj_track_id_list(sp, result):
  '''
  BPM or key or moodで続くトラックを決定したプレイリストの作成
  1. get_next_dj_dataでBPM,key,moodのいずれかが近いトラックを取得する。
  2. もしpriority_listのいずれにおいても条件を満たすトラックが存在しない場合は、残っているトラックからランダムに次のトラックを決定する。
  3. トラックを取得したらプレイリストのトラック情報を含むdataframe df_cpからそのトラックを消去する。
  5. 1.~3.をdf_cp内のトラックが無くなるまで実行する。
  '''

  # プレイリスト内の曲の情報を取得
  df = get_track_data(sp, result)
  priority_list = ['BPM','key','mood']
  index = 0

  df_cp = df[1:]
  df_dj = df.head(1)
  while df_cp.index.values.size >= 1:
    random.shuffle(priority_list)
    df_cp, df_dj, check = get_next_dj_data(df_cp, df_dj, priority_list)
    if check == False:
      row = df_cp.sample()
      idx = row.index.values[0]
      df_dj.loc[idx] = row.loc[idx]
      df_cp = df_cp.drop(index=idx, inplace=False)
  
  return df_dj

  
def make_dj_playlist(sp, df_dj):
  try:
    playlist = sp.user_playlist_create(config.USER_NAME,'DJ_ordered_'+config.PLAYLIST_NAME)

    # 100曲超のトラックを一度にプレイリストに追加しようとするとエラーが発生するため
    # 参考：https://zenn.dev/coveringnumber/articles/b7fd17323699c0
    chunk_size = 100
    id_list = df_dj.index.values.tolist()
    for i in range(0, len(id_list), chunk_size):
        ids_chunk = id_list[i:i+chunk_size]
        sp.user_playlist_add_tracks(config.USER_NAME, playlist['id'], ids_chunk)
  except Exception as e:
      print(e)
