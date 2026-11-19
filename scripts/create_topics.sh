#!/usr/bin/env bash
set -euo pipefail
COMPOSE="docker compose -f infra/docker-compose.yml"
for t in transactions fraud-alerts; do
  $COMPOSE exec kafka kafka-topics --bootstrap-server kafka:29092 \
    --create --if-not-exists --topic "$t" --partitions 3 --replication-factor 1
done
