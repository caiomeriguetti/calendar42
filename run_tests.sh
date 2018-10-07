#!/bin/bash

docker-compose run rest-api-test-runner bash -c "cd /src/rest-api/code && export PYTHONPATH=/src/rest-api/code && python -m unittest tests.PathTestCase"