import zipfile
import argparse
import pandas as pd
import json

# 引数の処理
parser = argparse.ArgumentParser(description="GTFS(ZIPファイル)をGeoJSONに変換")
parser.add_argument("--gtfs", default="./gtfs/nakatsugawa_GTFS.zip", help="gtfs file (zip file)")
parser.add_argument("--tmp", default="./tmp", help="directory for unzipped files")
parser.add_argument("--json", default="./json/nakatsugawa_GTFS.json", help="output geojson file")
args = parser.parse_args()

GTFS_FILE = args.gtfs
TMP_DIR = args.tmp
JSON_FILE = args.json

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

# バス停データの処理
stops_csv = pd.read_csv(stops_file)

stop_list = []

for index, record in stops_csv.iterrows():
    stop_id = record["stop_id"]
    stop_name = record["stop_name"]
    stop_lat = record["stop_lat"]
    stop_lon = record["stop_lon"]
    print(f"{stop_id} {stop_name} {stop_lat} {stop_lon}")

    stop = {
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

    stop_list.append(stop)

# GeoJSONの生成
geojson = {
    "type": "FeatureCollection",
    "features": stop_list
}
    
with open(JSON_FILE, "w") as file:
    json.dump(geojson, file, ensure_ascii=False)
    print(f"[save as {JSON_FILE}]")    
