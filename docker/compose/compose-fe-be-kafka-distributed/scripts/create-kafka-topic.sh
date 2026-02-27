#!/bin/bash

topic=test
cont=kafka-0
port=9092

while [[ $# -gt 0 ]]; do
  case "$1" in
    -t|--topic)
      topic="$2"
      shift 2
      ;;
    -c|--container)
      cont="$2"
      shift 2
      ;;
    -p|--port)
      port="$2"
      shift 2
      ;;
  esac
done

docker compose exec -i $cont /opt/kafka/bin/kafka-topics.sh --create --topic $topic --bootstrap-server localhost:$port
