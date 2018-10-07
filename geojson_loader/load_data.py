import json
import sys
sys.path.append('/src/rest-api/code')
from pymongo import GEOSPHERE

from app import db

with open('geojson_loader/arruamentoal.geojson', 'r') as f:
    geojson_data = json.loads(f.read())

features = geojson_data['features']

client = db.client()
db = client.street_data
db.features.drop()
db.points.drop()

print 'LOADING DATA'

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

print 'CREATING INDEXES'
db.points.create_index([('location', GEOSPHERE)])
