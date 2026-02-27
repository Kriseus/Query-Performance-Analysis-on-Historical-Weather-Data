#!/bin/bash

kafhost="kafka-0"

while getopts "k:h:" opt; do
  case $opt in
    k)
      kafhost="$OPTARG"
      ;;
    h) 
      echo -e " -k - kafka broker host"
  esac
done

echo -e \
"bootstrap.servers="$kafhost":9092\n\
offset.storage.file.filename=/tmp/connect.offsets\n\
offset.flush.interval.ms=10000\n\
key.converter=org.apache.kafka.connect.json.JsonConverter\n\
value.converter=org.apache.kafka.connect.json.JsonConverter\n\
key.converter.schemas.enable=true\n\
value.converter.schemas.enable=false\n\
plugin.path=/home/appuser/connector/starrocks-kafka-connector-1.0.4"\
> /opt/kafka/config/connect-standalone.properties
