#!/bin/bash

port=9092
topic=test
cont=kafka-0

while [[ $# -gt 0 ]]; do 
  case $1 in 
    -t|--topic)
      topic="$2"
      shift 2
      ;;
    -c|--container)
      cont="$2"
      shift 2
      ;;
    -p|port)
      port="$2"
      shift 2
      ;;
    -h|--help)
      echo -e " -t --topic - topic to add events \n -c --container - kafka broker container \n -p --port - port identifier"
  esac
done

docker compose exec -i $cont /opt/kafka/bin/kafka-console-producer.sh --topic $topic --bootstrap-server localhost:$port
