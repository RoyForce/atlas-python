#!/bin/bash

# Exit in case of error
set -e

docker-compose down

docker-compose build

docker-compose up -d

sleep 5;

docker-compose run --rm backend alembic upgrade head