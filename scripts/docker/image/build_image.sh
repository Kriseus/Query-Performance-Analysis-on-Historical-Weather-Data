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
IMAGE_DIR="$(echo "$json" | jq -r '.ImageDir')"
NAME="$(echo "$json" | jq -r '.Name')"

FULL_IMAGE_PATH="$ROOT_DIR/docker/images/$IMAGE_DIR"

docker build -t $NAME $FULL_IMAGE_PATH
