#!/bin/bash

docker-compose run rest-api-test-runner bash -c "export PYTHONPATH=rest-api/code && python -m unittest tests.PathTestCase"