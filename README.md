# GTFSConverter

任意のZIP圧縮されたGTFSファイルを，バス停(stops.geojson)，経路(routes.geojson)，時刻表(timetable.json)を表すJSONファイルに変換します．バス停と経路は[GeoJSON](https://geojson.org/)に従い，それぞれ **Point** と **LineString** で表されます．

## 使い方

Pythonで下記のコマンドを実行します．`--gtfs`はZIP圧縮されたGTFSファイルを指定します．

```
$python GTFSConverter --gtfs GTFSファイル
```

ZIP圧縮されたファイルを解凍するフォルダを`--tmp_dir`，JSONファイルを出力するフォルダを`json-dir`で指定します．

```
$python GTFSConverter --gtfs GTFSファイル --tmp_dir TMPフォルダ --json_dir JSONフォルダ
```
## フォーマット

### stops.geojson

```
{
	"type": "FeatureCollection", 
	"features": [{
		"type": "Feature", 
		"geometry": {
			"type": "Point", 
			"coordinates": [137.53108999999998, 35.51343]
		}, 
		"properties": {
			"stop_id": "1001_01", 
			"stop_name": "落合事務所"
		}
	}]
}
```

### routes.geojson

```
{
	"type": "FeatureCollection", 
	"features": [{
		"type": "Feature", 
		"geometry": {
			"type": "LineString", 
			"coordinates": [[137.45296000000002, 35.56013], [137.45127, 35.562909999999995], [137.44947, 35.56576], [137.4458, 35.56394], [137.43591, 35.56725], [137.43107, 35.56824], [137.4322, 35.57117], [137.43622, 35.57302], [137.44316, 35.57414], [137.44848000000002, 35.58133], [137.45148999999998, 35.58682], [137.45325, 35.58938], [137.43902, 35.59666], [137.42727, 35.59877], [137.40798, 35.59629], [137.40502, 35.596], [137.39743, 35.59515], [137.41101, 35.60464]]}, 
		"properties": {
			"trip_id": "10福岡金_08時32分_系統641001", 
			"stop_headsign": "新田方面", 
			"arrival_time": ["08:32:00", "08:34:00", "08:35:00", "08:36:00", "08:38:00", "08:39:00", "08:41:00", "08:42:00", "08:43:00", "08:45:00", "08:46:00", "08:47:00", "08:50:00", "08:52:00", "08:56:00", "08:57:00", "09:02:00", "09:07:00"], 
			"departure_time": ["08:32:00", "08:34:00", "08:35:00", "08:36:00", "08:38:00", "08:39:00", "08:41:00", "08:42:00", "08:43:00", "08:45:00", "08:46:00", "08:47:00", "08:50:00", "08:52:00", "08:56:00", "08:57:00", "09:02:00", "09:07:00"], "stop_id": ["6001_01", "6052_01", "6053_01", "6054_01", "6055_01", "6056_01", "6057_01", "6058_01", "6059_01", "6060_01", "6061_01", "6062_01", "6063_01", "6064_01", "6065_01", "6066_01", "6067_01", "6068_01"], 
			"stop_sequence": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
		}
	}]
}
```
