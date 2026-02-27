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
      echo -e " -t --topic - topic to delete \n -p --port - port identifier" 
      exit
      ;;
  esac
done

/opt/kafka/bin/kafka-topics.sh --bootstrap-server $kafhost:$port --delete --topic $topic