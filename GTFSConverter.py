import zipfile
import argparse
import pandas as pd
import json

# 引数の処理
parser = argparse.ArgumentParser(description="GTFS(ZIPファイル)をGeoJSONに変換")
parser.add_argument("--gtfs", default="./gtfs/nakatsugawa_GTFS.zip", help="gtfs file (zip file)")
parser.add_argument("--tmp_dir", default="./tmp/", help="directory for unzipped files")
parser.add_argument("--json_dir", default="./json/", help="output geojson file")
args = parser.parse_args()

GTFS_FILE = args.gtfs
TMP_DIR = args.tmp_dir
JSON_DIR = args.json_dir

# ZIPファイルの展開
zip_file = zipfile.ZipFile(GTFS_FILE)
#calendar_file = zip_file.extract("calendar.txt", TMP_DIR)
#calendar_dates_file = zip_file.extract("calendar_dates.txt", TMP_DIR)
#fare_attributes_file = zip_file.extract("fare_attributes.txt", TMP_DIR)
#fare_rules_file = zip_file.extract("fare_rules.txt", TMP_DIR)
#feed_info_file = zip_file.extract("feed_info.txt", TMP_DIR)
routes_file = zip_file.extract("routes.txt", TMP_DIR)
stop_times_file = zip_file.extract("stop_times.txt", TMP_DIR)
stops_file = zip_file.extract("stops.txt", TMP_DIR)
#translations_file = zip_file.extract("translations.txt", TMP_DIR)
trips_file = zip_file.extract("trips.txt", TMP_DIR)
#agency_file = zip_file.extract("agency.txt", TMP_DIR)

#--------------------------------------------------
# バス停データ（GeoJSON）の処理

stops_csv = pd.read_csv(stops_file)

stop_dict = {}

for index, record in stops_csv.iterrows():
    stop_id = record["stop_id"]
    stop_name = record["stop_name"]
    stop_lat = record["stop_lat"]
    stop_lon = record["stop_lon"]
    #print(f"stop_id={stop_id} stop_name={stop_name} stop_lat={stop_lat} stop_lon={stop_lon}")

    stop_dict[stop_id] = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [stop_lon, stop_lat]
        },
        "properties": {
            "stop_id": stop_id,
            "stop_name": stop_name
        }
    }

# GeoJSONの生成
geojson = {
    "type": "FeatureCollection",
    "features": list(stop_dict.values())
}

# ファイル出力
filename =  JSON_DIR + "stops.geojson"
with open(filename, "w") as file:
    json.dump(geojson, file, ensure_ascii=False)
    print(f"[save as {filename}]")
#--------------------------------------------------

#--------------------------------------------------
# トリップデータの処理

trip_names_csv = pd.read_csv(trips_file)

trip_name_dic = {}

for index, record in trip_names_csv.iterrows():
    route_id = record["route_id"]
    service_id = record["service_id"]
    trip_id = record["trip_id"]
    trip_headsign = record["trip_headsign"]
    #print(f"route_id={route_id} service_id={service_id} trip_id={trip_id} trip_headsign={trip_headsign}")

    trip_name = {
        "route_id": route_id,
        "service_id": service_id,
        "trip_id": trip_id,
        "trip_headsign": trip_headsign
    }

    trip_name_dic[trip_id] = trip_name

#--------------------------------------------------

#--------------------------------------------------
# 路線名の処理

route_names_csv = pd.read_csv(routes_file)

route_name_dic = {}

for index, record in route_names_csv.iterrows():
    route_id = record["route_id"]
    route_long_name = record["route_long_name"]
    route_color = record["route_color"]
    #print(f"route_id={route_id} route_long_name={route_long_name} route_color={route_color}")

    route_name = {
        "route_id": route_id,
        "route_long_name": route_long_name,
        "route_color": route_color
    }

    route_name_dic[route_id] = route_name

#--------------------------------------------------

#--------------------------------------------------
# 経路データ（GeoJSON）の処理

trips_csv = pd.read_csv(stop_times_file)

trip_dic = {}

# データを辞書に格納
for index, record in trips_csv.iterrows():
    trip_id = record["trip_id"]
    arrival_time = record["arrival_time"]
    departure_time = record["departure_time"]
    stop_id = record["stop_id"]
    stop_sequence = int(record["stop_sequence"])
    stop_headsign = record["stop_headsign"]
    #print(f"trip_id={trip_id} arrival_time={arrival_time} departure_time={departure_time} stop_id={stop_id} stop_sequence={stop_sequence} stop_headsign={stop_headsign}")

    if(not(trip_id in trip_dic)):
        trip_dic[trip_id] = {
            "trip_id": trip_id,
            "stop_headsign": stop_headsign,
            "arrival_time": [arrival_time],
            "departure_time": [departure_time],
            "stop_id": [stop_id],
            "stop_sequence": [stop_sequence]
        }
    else:        
        trip_dic[trip_id]["arrival_time"].append(arrival_time)
        trip_dic[trip_id]["departure_time"].append(departure_time)
        trip_dic[trip_id]["stop_id"].append(stop_id)
        trip_dic[trip_id]["stop_sequence"].append(stop_sequence)

# 経路データの生成

route_dic = {}

for key in trip_dic.keys():

    trip = trip_dic[key]       

    coordinates = []
    for stop_id in trip["stop_id"]:
        latlng = stop_dict[stop_id]["geometry"]["coordinates"]
        coordinates.append(latlng)
    
    route = {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": coordinates
        },
        "properties": {
            "trip_id": trip["trip_id"],
            "service_id": trip_name_dic[trip["trip_id"]]["service_id"],
            "route_long_name": route_name_dic[trip_name_dic[trip["trip_id"]]["route_id"]]["route_long_name"],
            "trip_headsign": trip_name_dic[trip["trip_id"]]["trip_headsign"],            
            "stop_headsign": trip["stop_headsign"]
        }
    }

    route_dic[trip["trip_id"]] = route

# GeoJSONの生成
geojson = {
    "type": "FeatureCollection",
    "features": list(route_dic.values())
}

# ファイル出力
filename =  JSON_DIR + "routes.geojson"
with open(filename, "w") as file:
    json.dump(geojson, file, ensure_ascii=False)
    print(f"[save as {filename}]")
#--------------------------------------------------    

#--------------------------------------------------
# 経路データ（JSON）の処理

route_dic = {}

for key in trip_dic.keys():

    trip = trip_dic[key]

    for arrival_time, departure_time, stop_id, stop_sequence in zip(trip["arrival_time"], trip["departure_time"], trip["stop_id"], trip["stop_sequence"]):

        record = {
            "arrival_time": arrival_time,
            "departure_time": departure_time,
            "stop_id": stop_id,
            "stop_sequence": stop_sequence        
        }
        
        if(trip["trip_id"] in route_dic):
            route_dic[trip["trip_id"]]["records"].append(record)
        else:
        
            route = {
                "trip_id": trip["trip_id"],
                "service_id": trip_name_dic[trip["trip_id"]]["service_id"],
                "route_long_name": route_name_dic[trip_name_dic[trip["trip_id"]]["route_id"]]["route_long_name"],
                "trip_headsign": trip_name_dic[trip["trip_id"]]["trip_headsign"],            
                "stop_headsign": trip["stop_headsign"],
                "records": [record]
            }

            route_dic[trip["trip_id"]] = route

# ファイル出力
filename =  JSON_DIR + "routes.json"
with open(filename, "w") as file:
    json.dump(route_dic, file, ensure_ascii=False)
    print(f"[save as {filename}]")
#--------------------------------------------------

#--------------------------------------------------
# 時刻表データ（JSON）の処理

timetable_list = {}

for key in trip_dic.keys():

    trip = trip_dic[key]       

    for stop_id, stop_sequence in zip(trip["stop_id"], trip["stop_sequence"]):
        stop_name = stop_dict[stop_id]["properties"]["stop_name"]
        stop_sequence = int(stop_sequence) - 1

        record = {
            "trip_id": trip["trip_id"],
            "service_id": trip_name_dic[trip["trip_id"]]["service_id"],
            "route_long_name": route_name_dic[trip_name_dic[trip["trip_id"]]["route_id"]]["route_long_name"],
            "trip_headsign": trip_name_dic[trip["trip_id"]]["trip_headsign"],                        
            "stop_headsign": trip["stop_headsign"],
            "arrival_time": trip["arrival_time"][stop_sequence],
            "departure_time": trip["departure_time"][stop_sequence],
        }
        
        if(stop_id in timetable_list):
            timetable_list[stop_id]["records"].append(record)
        else:            
            timetable_list[stop_id] = {
                "stop_id": stop_id,
                "stop_name": stop_name,
                "records": [record]
            }

# 到着時刻でソート
for key in timetable_list.keys():
    timetable_list[key]["records"] = sorted(timetable_list[key]["records"], key=lambda x: x["arrival_time"])
    
# ファイル出力
filename =  JSON_DIR + "timetable.json"
with open(filename, "w") as file:
    json.dump(timetable_list, file, ensure_ascii=False)
    print(f"[save as {filename}]")
#--------------------------------------------------
