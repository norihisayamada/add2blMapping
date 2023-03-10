import folium
import pandas as pd
import requests
import streamlit as st
from streamlit_folium import folium_static
import urllib.request

st.title('国土地理院APIを用いて住所から緯度経度に変換するアプリです')
st.header('住所の緯度経度を地図に表示します')

#開発環境
st.caption('開発環境')
env = pd.read_csv('enviroment.csv')
st.dataframe(env)

# 国土地理院API
GeospatialUrl = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="

# データフレーム作成/ファイルの読み込み
upload_file = st.file_uploader('ファイルのアップロード', type=['csv', 'txt'])
# if upload_file is not None:
    # content = upload_file.read()
    # print(content)
df = pd.read_csv(upload_file)


# df = pd.read_csv('./sample_address.csv')
st.text('サンプルデータを使用（UAV関係会社住所)')
"""国土地理院APIを用いて住所から緯度経度に変換する"""
st.write(df)


# 国土地理院APIより住所→緯度経度に変換
# def add2bl(df):
lat_list = []
lng_list = []
for index, row in df.iterrows():
    s_quote = urllib.parse.quote(row.住所)
    response = requests.get(GeospatialUrl + s_quote)
    # print(response.json()[0])
    try:
        lat_list.append(response.json()[0]["geometry"]["coordinates"][1])
        lng_list.append(response.json()[0]["geometry"]["coordinates"][0])
    except Exception as e:
        print(e)


# inputデータに緯度経度を追加する
# def addBL(df):
    df_new = df.copy()
    try:
        df_new['lat'] = lat_list
        df_new['lng'] = lng_list
    except Exception as e:
        print(e)
# csvに結果を保存する
df_new.to_csv('./result_add2latlng.csv', encoding='UTF-8', index=False)


# 会社住所をmapに描画する
m = folium.Map(location=[df_new[0:1].lat, df_new[0:1].lng], tiles='OpenStreetMap', zoom_start=10)
for i, marker in df_new.iterrows():
    name='Location:'+str(i)
    lat = marker.lat
    lon = marker.lng
    popup ="<strong>{0}</strong><br>Lat:{1:.3f}<br>Long:{2:.3f}".format(name, lat, lon)
    folium.Marker(location=[lat, lon], popup=popup, icon=folium.Icon(color='lightgreen')).add_to(m)

# HTML出力（ブラウザで見る場合はchromeなどでブラウジングすることもできます）
m.save('./mapping' + '.html')

st.write('地図に表示しますか？')
if st.button('開始'):
    'mapping...'
    folium_static(m)

#ref
# st.text('C:\\Users\sus44\PycharmProjects\surveybl2xy')
# st.text('csv形式で保存された住所を緯度経度を付加します')
# st.caption('This is a string that explains something above.')
# st.caption('A caption with _italics_ :blue[colors] and emojis :sunglasses:')

