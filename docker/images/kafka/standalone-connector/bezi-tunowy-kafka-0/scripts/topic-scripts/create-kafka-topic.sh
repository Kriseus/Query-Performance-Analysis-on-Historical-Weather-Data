#!/bin/bash

topic=test
port=9092
kafhost="kafka-0"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -t|--topic)
      topic="$2"
      shift 2
      ;;
    -p|--port)
      port="$2"
      shift 2
      ;;
    -h|--help)
      echo -e " -t --topic - topic to create \n -c --container - container of kafka broker \n -p --port - port identifier" 
      exit
      ;;
  esac
done

/opt/kafka/bin/kafka-topics.sh --create --topic $topic --bootstrap-server $kafhost:$port