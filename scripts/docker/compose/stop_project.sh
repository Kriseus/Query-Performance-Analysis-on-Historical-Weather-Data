#!/bin/bash

ROOT_DIR="$(realpath $(dirname $0))"
suffix=".sh"
config_suffix=".json"
filename="$(basename ${0})"

while [ "$(basename $ROOT_DIR)" != "Project" ]; do
  ROOT_DIR="${ROOT_DIR%/$(basename $ROOT_DIR)}"
done

JSN_DIR="$ROOT_DIR/jsons/parameters_values/"

CONFIG_FILE="${filename%$suffix}$config_suffix"
CONFIG="$JSN_DIR$CONFIG_FILE"
json=$(cat $CONFIG)
COMPOSE_PATH="$ROOT_DIR/docker/compose/$(echo "$json" | jq -r '.ComposeDir')/docker-compose.yml"

docker compose -f $COMPOSE_PATH stop