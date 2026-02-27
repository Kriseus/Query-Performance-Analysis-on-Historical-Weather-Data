#!/bin/bash

CLASSPATH=/home/appuser/connector/starrocks-kafka-connector-1.0.4/* \
/opt/kafka/bin/connect-standalone.sh \
/opt/kafka/config/connect-standalone.properties \
/opt/kafka/config/connect-starrocks-sink.properties > ~/log/kafka-connector.log 