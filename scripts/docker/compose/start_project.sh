#!/bin/bash

ROOT_DIR="$(realpath $(dirname $0))"
suffix=".sh"
prefix="./"
config_suffix=".json"
filename="${0#$prefix}"

while [ "$(basename $ROOT_DIR)" != "Project" ]; do
  ROOT_DIR="${ROOT_DIR%/$(basename $ROOT_DIR)}"
done

JSN_DIR="$ROOT_DIR/jsons/parameters_value"

CONFIG_FILE="${filename%$suffix}$config_suffix"
CONFIG="$JSN_DIR$CONFIG_FILE"

json=$(cat $CONFIG)
COMPOSE_PATH=$(echo "$json" | jq -r '.composePath')

docker compose -f $COMPOSE_PATH up
