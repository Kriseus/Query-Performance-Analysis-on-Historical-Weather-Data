#!/bin/bash

topic='test'
port='9092'
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
      echo -e " -t --topic - topic to add events \n -p --port - port identifier" 
      exit
      ;;
  esac
done

/opt/kafka/bin/kafka-console-producer.sh --topic $topic --bootstrap-server $kafhost:$port