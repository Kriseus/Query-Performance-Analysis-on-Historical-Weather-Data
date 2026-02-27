FROM starrocks/be-ubuntu:3.5-latest

USER root
RUN mkdir -p /home/user/config
COPY ./scripts/config-be.sh /home/user/config/config-be.sh
RUN chmod 777 /home/user/config/config-be.sh

CMD ["/opt/starrocks/be/bin/start_be.sh"]
