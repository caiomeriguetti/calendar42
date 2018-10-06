#!/bin/bash

docker-compose up -d geodb
docker-compose run geojson-loader bash -c "python geojson_loader/load_data.py"