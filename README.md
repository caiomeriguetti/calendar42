# the app

Jane is delivering letters in Alagoas, Brazil.

The idea is to provide an app where jane can calculate routes for delivering letters.
First she has to click on the places where she must pass throught to deliver letters.
To do so she needs to press ENTER then click on the places in the map. After she has
choosen the places she just press ENTER again and the system will calculate the route.

# how to run the app

the app is composed by a frontend and a rest api. in the project root just run

```docker-compose up -d --force-recreate --build```

# how to load the data into database 

just run 

```./load_db.sh```

# pathfinder

the rest-api exposes an endpoint for calculating a path that contains N points

```/best-path/lat1,lng1;...;latN,lngN```

the red markers represent the places Jane must go to deliver letters and the green ones are extra points since jane like to meet new places


