#!/bin/bash

topic="test"
table="test_tbl"
user="user1"
passwd=123456
database="example_db"
fehost="starrocks-fe"

while getopts "t:T:u:p:d:f:h:" opt; do
  case $opt in
    t)
      topic="$OPTARG"
      ;;
    T)
      table="$OPTARG"
      ;;
    u)
      user="$OPTARG"
      ;;
    p)
      passwd="$OPTARG"
      ;;
    d)
      database="$OPTARG"
      ;;
    f)
      fehost="$OPTARG"
      ;;
    h)
      echo -e " -t - Kafka topic \n -T - SR table \n -u - SR user \n -p - password for SR user \n -d - SR database \n -f - FE SR host"
      exit
  esac
done

echo -e \
"name=starrocks-kafka-connector\n\
connector.class=com.starrocks.connector.kafka.StarRocksSinkConnector\n\
topics="$topic"\n\
key.converter=org.apache.kafka.connect.json.JsonConverter\n\
value.converter=org.apache.kafka.connect.json.JsonConverter\n\
key.converter.schemas.enable=true\n\
value.converter.schemas.enable=false\n\
starrocks.http.url="$fehost":8030\n\
starrocks.topic2table.map=""$topic":"$table""\n\
starrocks.username="$user"\n\
starrocks.password="$passwd"\n\
starrocks.database.name="$database"\n\
sink.properties.strip_outer_array=true"\
> /opt/kafka/config/connect-starrocks-sink.properties
