# GTFSConverter

任意のZIP圧縮されたGTFSファイルを，バス停(stops.geojson)，経路(routes.geojson)，時刻表(timetable.json)を表すJSONファイルに変換します．バス停と経路は[GeoJSON](https://geojson.org/)フォーマットに従い，それぞれ **Point** と **LineString** で表されます．一方，時刻表は独自のフォーマットです．

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
			"service_id": "福岡金", 
			"route_long_name": "新田線", 
			"trip_headsign": "新田方面",						
			"stop_headsign": "新田方面", 
			"arrival_time": ["08:32:00", "08:34:00", "08:35:00", "08:36:00", "08:38:00", "08:39:00", "08:41:00", "08:42:00", "08:43:00", "08:45:00", "08:46:00", "08:47:00", "08:50:00", "08:52:00", "08:56:00", "08:57:00", "09:02:00", "09:07:00"], 
			"departure_time": ["08:32:00", "08:34:00", "08:35:00", "08:36:00", "08:38:00", "08:39:00", "08:41:00", "08:42:00", "08:43:00", "08:45:00", "08:46:00", "08:47:00", "08:50:00", "08:52:00", "08:56:00", "08:57:00", "09:02:00", "09:07:00"], 
			"stop_id": ["6001_01", "6052_01", "6053_01", "6054_01", "6055_01", "6056_01", "6057_01", "6058_01", "6059_01", "6060_01", "6061_01", "6062_01", "6063_01", "6064_01", "6065_01", "6066_01", "6067_01", "6068_01"], 
			"stop_sequence": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
		}
	}]
}
```

### timetable.json

```
{
	'6001_01':	
	{
		'stop_id': '6001_01', 
		'stop_name': '総合福祉センター', 
		'records': [{'trip_id': '10福岡金_08時32分_系統641001', "service_id": "福岡金", "route_long_name": "新田線", "trip_headsign": "新田方面", 'stop_headsign': '新田方面', 'arrival_time': '08:32:00', 'departure_time': '08:32:00'}, {'trip_id': '8福岡木_08時40分_系統611001', 'stop_headsign': '若山方面', 'arrival_time': '08:40:00', 'departure_time': '08:40:00'}, {'trip_id': '9福岡水_08時45分_系統621001', 'stop_headsign': '本郷方面', 'arrival_time': '08:45:00', 'departure_time': '08:45:00'}, {'trip_id': '7福岡火_08時50分_系統601001', 'stop_headsign': '矢平方面', 'arrival_time': '08:50:00', 'departure_time': '08:50:00'}, {'trip_id': '9福岡水_08時59分_系統622001', 'stop_headsign': '総合福祉センター', 'arrival_time': '09:12:00', 'departure_time': '09:12:00'}, {'trip_id': '8福岡木_09時00分_系統612001', 'stop_headsign': '総合福祉センター', 'arrival_time': '09:19:00', 'departure_time': '09:19:00'}, {'trip_id': '9福岡水_09時25分_系統631001', 'stop_headsign': '上之平・下組方面', 'arrival_time': '09:25:00', 'departure_time': '09:25:00'}, {'trip_id': '8福岡木_09時40分_系統601001', 'stop_headsign': '矢平方面', 'arrival_time': '09:40:00', 'departure_time': '09:40:00'}, {'trip_id': '10福岡金_09時10分_系統642001', 'stop_headsign': '総合福祉センター', 'arrival_time': '09:44:00', 'departure_time': '09:44:00'}, {'trip_id': '7福岡火_09時20分_系統602001', 'stop_headsign': '総合福祉センター', 'arrival_time': '09:49:00', 'departure_time': '09:49:00'}, {'trip_id': '9福岡水_09時25分_系統631001', 'stop_headsign': '上之平・下組方面', 'arrival_time': '09:50:00', 'departure_time': '09:50:00'}, {'trip_id': '7福岡火_09時55分_系統611001', 'stop_headsign': '若山方面', 'arrival_time': '09:55:00', 'departure_time': '09:55:00'}, {'trip_id': '10福岡金_10時15分_系統631001', 'stop_headsign': '上之平・下組方面', 'arrival_time': '10:15:00', 'departure_time': '10:15:00'}, {'trip_id': '9福岡水_10時15分_系統641001', 'stop_headsign': '新田方面', 'arrival_time': '10:15:00', 'departure_time': '10:15:00'}, {'trip_id': '7福岡火_10時15分_系統612001', 'stop_headsign': '総合福祉センター', 'arrival_time': '10:34:00', 'departure_time': '10:34:00'}, {'trip_id': '8福岡木_10時10分_系統602001', 'stop_headsign': '総合福祉センター', 'arrival_time': '10:39:00', 'departure_time': '10:39:00'}, {'trip_id': '10福岡金_10時15分_系統631001', 'stop_headsign': '上之平・下組方面', 'arrival_time': '10:40:00', 'departure_time': '10:40:00'}, {'trip_id': '10福岡金_10時55分_系統621001', 'stop_headsign': '本郷方面', 'arrival_time': '10:55:00', 'departure_time': '10:55:00'}, {'trip_id': '10福岡金_11時09分_系統622001', 'stop_headsign': '総合福祉センター', 'arrival_time': '11:22:00', 'departure_time': '11:22:00'}, {'trip_id': '9福岡水_10時53分_系統642001', 'stop_headsign': '総合福祉センター', 'arrival_time': '11:27:00', 'departure_time': '11:27:00'}, {'trip_id': '10福岡金_12時42分_系統641001', 'stop_headsign': '新田方面', 'arrival_time': '12:42:00', 'departure_time': '12:42:00'}, {'trip_id': '9福岡水_13時00分_系統621001', 'stop_headsign': '本郷方面', 'arrival_time': '13:00:00', 'departure_time': '13:00:00'}, {'trip_id': '9福岡水_13時14分_系統622001', 'stop_headsign': '総合福祉センター', 'arrival_time': '13:27:00', 'departure_time': '13:27:00'}, {'trip_id': '10福岡金_13時20分_系統642001', 'stop_headsign': '総合福祉センター', 'arrival_time': '13:54:00', 'departure_time': '13:54:00'}, {'trip_id': '10福岡金_14時00分_系統632001', 'stop_headsign': '上之平・下組方面', 'arrival_time': '14:00:00', 'departure_time': '14:00:00'}, {'trip_id': '7福岡火_14時00分_系統601001', 'stop_headsign': '矢平方面', 'arrival_time': '14:00:00', 'departure_time': '14:00:00'}, {'trip_id': '8福岡木_14時00分_系統611001', 'stop_headsign': '若山方面', 'arrival_time': '14:00:00', 'departure_time': '14:00:00'}, {'trip_id': '9福岡水_14時00分_系統632001', 'stop_headsign': '上之平・下組方面', 'arrival_time': '14:00:00', 'departure_time': '14:00:00'}, {'trip_id': '10福岡金_14時00分_系統632001', 'stop_headsign': '上之平・下組方面', 'arrival_time': '14:25:00', 'departure_time': '14:25:00'}, {'trip_id': '9福岡水_14時00分_系統632001', 'stop_headsign': '上之平・下組方面', 'arrival_time': '14:25:00', 'departure_time': '14:25:00'}, {'trip_id': '8福岡木_14時20分_系統612001', 'stop_headsign': '総合福祉センター', 'arrival_time': '14:39:00', 'departure_time': '14:39:00'}, {'trip_id': '7福岡火_14時30分_系統602001', 'stop_headsign': '総合福祉センター', 'arrival_time': '14:59:00', 'departure_time': '14:59:00'}, {'trip_id': '10福岡金_15時15分_系統621001', 'stop_headsign': '本郷方面', 'arrival_time': '15:15:00', 'departure_time': '15:15:00'}, {'trip_id': '7福岡火_15時15分_系統611001', 'stop_headsign': '若山方面', 'arrival_time': '15:15:00', 'departure_time': '15:15:00'}, {'trip_id': '8福岡木_15時15分_系統601001', 'stop_headsign': '矢平方面', 'arrival_time': '15:15:00', 'departure_time': '15:15:00'}, {'trip_id': '9福岡水_15時15分_系統641001', 'stop_headsign': '新田方面', 'arrival_time': '15:15:00', 'departure_time': '15:15:00'}, {'trip_id': '10福岡金_15時29分_系統622001', 'stop_headsign': '総合福祉センター', 'arrival_time': '15:42:00', 'departure_time': '15:42:00'}, {'trip_id': '7福岡火_15時35分_系統612001', 'stop_headsign': '総合福祉センター', 'arrival_time': '15:54:00', 'departure_time': '15:54:00'}, {'trip_id': '8福岡木_15時45分_系統602001', 'stop_headsign': '総合福祉センター', 'arrival_time': '16:14:00', 'departure_time': '16:14:00'}, {'trip_id': '9福岡水_15時53分_系統642001', 'stop_headsign': '総合福祉センター', 'arrival_time': '16:27:00', 'departure_time': '16:27:00'}]
	}
}
```
