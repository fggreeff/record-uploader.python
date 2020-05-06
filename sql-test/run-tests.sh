#!/bin/bash
set -e

export DOCKER_COMPOSE_FILE=./docker-compose.yml

docker-compose -f $DOCKER_COMPOSE_FILE down -v

docker-compose -f $DOCKER_COMPOSE_FILE build
docker-compose -f $DOCKER_COMPOSE_FILE up -d
sleep 5

TEST_STATUS=$(docker-compose -f "$DOCKER_COMPOSE_FILE" logs postgres | grep "Test Failed for SQL Query" | wc -l)

if [ "$TEST_STATUS" -gt 0 ]; then
  echo "Tests Failed! due to: "
  docker-compose -f "$DOCKER_COMPOSE_FILE" logs postgres
  exit 1
else
  echo "Tests Passed!"
  exit 0
fi