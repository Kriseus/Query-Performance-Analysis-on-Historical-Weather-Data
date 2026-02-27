#!/bin/bash

docker compose exec kafka-0 \
/opt/kafka/bin/connect-standalone.sh \
/opt/kafka/config/connect-standalone.properties \
/opt/kafka/config/connect-starrocks-sink.properties \
> ~/Bezi-Tunowy/Project/docker/compose/compose-fe-be-kafka/logs/kafka-connector.log
