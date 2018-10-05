import json
import sys
sys.path.append('.')
import db
with open('geojson/arruamentoal.geojson', 'r') as f:
    geojson_data = json.loads(f.read())

features = geojson_data['features']

client = db.client()
db = client.street_data
points = []
for feature in features:
    feature['geometry']['coords_dict'] = []
    for coordinate in feature['geometry']['coordinates']:
        lat = coordinate[1]
        lng = coordinate[0]
        feature['geometry']['coords_dict'].append({'lat': lat, 'lng': lng})
        points.append({'location': {'type': 'Point', 'coordinates': [lng, lat]}})

db.features.insert_many(features)
db.points.insert_many(points)


