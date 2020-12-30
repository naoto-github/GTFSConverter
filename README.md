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
