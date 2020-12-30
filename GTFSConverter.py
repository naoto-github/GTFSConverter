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
calendar_file = zip_file.extract("calendar.txt", TMP_DIR)
calendar_dates_file = zip_file.extract("calendar_dates.txt", TMP_DIR)
fare_attributes_file = zip_file.extract("fare_attributes.txt", TMP_DIR)
fare_rules_file = zip_file.extract("fare_rules.txt", TMP_DIR)
feed_info_file = zip_file.extract("feed_info.txt", TMP_DIR)
routes_file = zip_file.extract("routes.txt", TMP_DIR)
stop_times_file = zip_file.extract("stop_times.txt", TMP_DIR)
stops_file = zip_file.extract("stops.txt", TMP_DIR)
translations_file = zip_file.extract("translations.txt", TMP_DIR)
trips_file = zip_file.extract("trips.txt", TMP_DIR)
agency_file = zip_file.extract("agency.txt", TMP_DIR)

#--------------------------------------------------
# バス停データの処理

stops_csv = pd.read_csv(stops_file)

stop_dict = {}

for index, record in stops_csv.iterrows():
    stop_id = record["stop_id"]
    stop_name = record["stop_name"]
    stop_lat = record["stop_lat"]
    stop_lon = record["stop_lon"]
    #print(f"{stop_id} {stop_name} {stop_lat} {stop_lon}")

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
# 経路データの処理

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
    #print(f"{trip_id} {arrival_time} {departure_time} {stop_id} {stop_sequence} {stop_headsign}")

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
            "stop_headsign": trip["stop_headsign"],
            "arrival_time": trip["arrival_time"],
            "departure_time": trip["departure_time"],
            "stop_id": trip["stop_id"],
            "stop_sequence": trip["stop_sequence"]
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
# 時刻表の処理

timetable_list = {}

for key in trip_dic.keys():

    trip = trip_dic[key]       

    coordinates = []
    for stop_id, stop_sequence in zip(trip["stop_id"], trip["stop_sequence"]):
        stop_name = stop_dict[stop_id]["properties"]["stop_name"]
        stop_sequence = int(stop_sequence) - 1

        if(stop_id in timetable_list):
            timetable_list[stop_id]["trip_id"].append(trip["trip_id"])
            timetable_list[stop_id]["stop_headsign"].append(trip["stop_headsign"])
            timetable_list[stop_id]["arrival_time"].append(trip["arrival_time"][stop_sequence])
            timetable_list[stop_id]["departure_time"].append(trip["departure_time"][stop_sequence])
        else:            
            timetable_list[stop_id] = {
                "stop_id": stop_id,
                "stop_name": stop_name,
                "trip_id": [trip["trip_id"]],
                "stop_headsign": [trip["stop_headsign"]],
                "arrival_time": [trip["arrival_time"][stop_sequence]],
                "departure_time": [trip["departure_time"][stop_sequence]],
            }

# ファイル出力
filename =  JSON_DIR + "timetable.json"
with open(filename, "w") as file:
    json.dump(timetable_list, file, ensure_ascii=False)
    print(f"[save as {filename}]")
#--------------------------------------------------
