#!/usr/bin/env bash
# Đưa file PaySim lên HDFS
set -euo pipefail
COMPOSE="docker compose -f infra/docker-compose.yml"
CSV=$(ls data/raw/*.csv | head -n1)
$COMPOSE cp "$CSV" namenode:/tmp/paysim.csv
$COMPOSE exec namenode hdfs dfs -mkdir -p /data/raw/paysim /data/curated /checkpoints
$COMPOSE exec namenode hdfs dfs -put -f /tmp/paysim.csv /data/raw/paysim/
$COMPOSE exec namenode hdfs dfs -ls /data/raw/paysim
