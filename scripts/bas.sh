#!/bin/bash

ROOT_DIR="$(realpath $(dirname $0))"
suffix=".sh"
prefix="./"
filename="${0#$prefix}"

while [ "$(basename $ROOT_DIR)" != "Project" ]; do
  ROOT_DIR="${ROOT_DIR%/$(basename $ROOT_DIR)}"
done

echo $ROOT_DIR

JSN_DIR="$ROOT_DIR/jsons/"
echo $JSN_DIR
echo $0

CONFIG_FILE="${filename%$suffix}.json"
CONFIG="$JSN_DIR$CONFIG_FILE"

echo $CONFIG_FILE
echo $filename
echo $CONFIG

json=$(cat $CONFIG)
number=$(echo "$json" | jq -r '.value')
#names=$(echo "$json" | jq -r '.people[].name')

echo "Number of people: $number"
#echo "Names: $names"
