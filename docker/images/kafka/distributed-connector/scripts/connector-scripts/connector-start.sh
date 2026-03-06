#!/bin/bash

CLASSPATH=/home/appuser/connector/starrocks-kafka-connector-1.0.4/* \
/opt/kafka/bin/connect-distributed.sh \
/opt/kafka/config/connect-distributed.properties > ~/log/kafka-connector.log 
