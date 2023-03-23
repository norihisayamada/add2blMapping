import folium
import pandas as pd
import requests
import streamlit as st
from streamlit_folium import folium_static
import urllib.request

st.title('国土地理院APIを用いて、住所から緯度経度に変換するアプリです')
# env = pd.read_csv('project/enviroment.csv')
# st.dataframe(env)
# 国土地理院API
GeospatialUrl = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="
lat_list = []
lng_list = []

# 入力データの読み込み/データフレーム作成/
st.text('サンプル（京都おすすめ居酒屋）')
df = pd.read_csv('./kyoto.csv')
st.write(df)

# 国土地理院APIより住所→緯度経度に変換
class tranceBL:
    def trance(self):
        for index, row in df.iterrows():
            s_quote = urllib.parse.quote(row.住所)
            response = requests.get(GeospatialUrl + s_quote)
            print(response.json()[0])
            try:
                lat_list.append(response.json()[0]["geometry"]["coordinates"][1])
                lng_list.append(response.json()[0]["geometry"]["coordinates"][0])
            except Exception as e:
                print(e)

st.subheader("住所を緯度経度に変換します")
st.text('入力データの読込み')
if  st.button('file upload'):
    upload_file = st.file_uploader('ファイルのアップロード', type=['csv','xlsx'])
    if upload_file is not None:
        content = upload_file.read()
        df = pd.read_csv(content)
        st.write(df)

st.text('住所から緯度経度に変換')
st.button('tranceBL')
trance = tranceBL()
res = trance.trance()

# 入力データに緯度経度を追加する
df_new = df.copy()
try:
    df_new['lat'] = lat_list
    df_new['lng'] = lng_list
except Exception as e:
    print(e)

# 会社住所をmapに描画する
m = folium.Map(location=[df_new[0:1].lat, df_new[0:1].lng], tiles='OpenStreetMap', zoom_start=10)
for i, marker in df_new.iterrows():
    name='Location:'+str(marker)
    lat = marker.lat
    lon = marker.lng
    popup ="<strong>{0}</strong><br>Lat:{1:.3f}<br>Long:{2:.3f}".format(name, lat, lon)
    folium.Marker(location=[lat, lon], popup=popup, icon=folium.Icon(color='lightgreen')).add_to(m)

# HTML出力（ブラウザで見る場合はchromeなどでブラウジングすることもできます）
m.save('./mapping' + '.html')

st.subheader('地図に表示します')
if st.button('mapping'):
    folium_static(m)

# csvに結果を保存する
st.subheader('結果をダウンロードします')
df_new.to_csv('./result_add2latlng.csv', encoding='UTF-8', index=False)
