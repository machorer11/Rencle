#japan_bike_rental_map.htmlを表示するプログラム
#日本地図の上にポイントを指定できるプログラム
#そこを自転車の貸し出しポイントとして指定できる。その時に、料金設定、返却場所を指定できる。   
import folium
from folium.plugins import MarkerCluster
# 日本の地図の中心座標
japan_center = [36.2048, 138.2529]
# 地図の初期化
m = folium.Map(location=japan_center, zoom_start=5)
# マーカークラスターの初期化
marker_cluster = MarkerCluster().add_to(m)
# 自転車貸し出しポイントのデータ
rental_points = [
    {"name": "Tokyo Rental Point", "location": [35.6895, 139.6917], "price_per_hour": 300, "return_location": "Any rental point in Tokyo"},
    {"name": "Osaka Rental Point", "location": [34.6937, 135.5023], "price_per_hour": 250, "return_location": "Any rental point in Osaka"},
    {"name": "Kyoto Rental Point", "location": [35.0116, 135.7681], "price_per_hour": 200, "return_location": "Any rental point in Kyoto"},
]
# マーカーの追加
for point in rental_points: 
    popup_text = f"{point['name']}<br>Price per hour: ¥{point['price_per_hour']}<br>Return location: {point['return_location']}"
    folium.Marker(
        location=point["location"],
        popup=popup_text,
        icon=folium.Icon(color='blue', icon='bicycle', prefix='fa') 
    ).add_to(marker_cluster)
# 地図の保存
m.save("japan_bike_rental_map.html")
#日本地図の表示
import webbrowser
webbrowser.open("japan_bike_rental_map.html")
#マップ上にポイントを追加するプログラムを追加してください。　追加するときには、ポイントの名前、料金設定、返却場所を指定できるようにしてください

def add_rental_point(name, location, price_per_hour, return_location):
    popup_text = f"{name}<br>Price per hour: ¥{price_per_hour}<br>Return location: {return_location}"
    folium.Marker(
        location=location,
        popup=popup_text,
        icon=folium.Icon(color='blue', icon='bicycle', prefix='fa')
    ).add_to(marker_cluster)
    m.save("japan_bike_rental_map.html")
    webbrowser.open("japan_bike_rental_map.html")
#例として新しいポイントを追加
add_rental_point("Nagoya Rental Point", [35.1815, 136.9066], 220, "Any rental point in Nagoya")
#add_rental_point関数をmap上でいつでも呼び出して新しいポイントを追加できます

