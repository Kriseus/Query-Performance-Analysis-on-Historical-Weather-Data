FROM  apache/kafka:3.7.0

USER root

RUN mkdir -p /home/appuser/scripts
RUN mkdir -p /home/appuser/connector/
RUN mkdir -p /home/appuser/log/

# COPY ./scripts/conf-connect-StarRocks-Sink.sh /home/appuser/config/conf-connect-StarRocks-Sink.sh
# COPY ./scripts/conf-connect-Standalone.sh /home/appuser/config/conf-connect-Standalone.sh

COPY ./scripts /home/appuser/scripts
COPY ./connectors/starrocks-kafka-connector-1.0.4 /home/appuser/connector/starrocks-kafka-connector-1.0.4
COPY ./config/connect-standalone.properties /opt/kafka/config/connect-standalone.properties
COPY ./config/connect-starrocks-sink.properties /opt/kafka/config/connect-starrocks-sink.properties

RUN chmod -R 777 /home/appuser/scripts

USER appuser

CMD ["/etc/kafka/docker/run"]