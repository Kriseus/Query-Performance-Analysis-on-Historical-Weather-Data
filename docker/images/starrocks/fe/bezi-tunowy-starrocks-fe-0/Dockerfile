FROM starrocks/fe-ubuntu:3.5-latest

# RUN mkdir -p /home/user/vols/metadata

USER root

RUN mkdir -p /home/user/vols
RUN mkdir -p /home/user/config

COPY  ./scripts/config-fe.sh /home/user/config/config-fe.sh

RUN chmod 777 /home/user/config/config-fe.sh

CMD ["/opt/starrocks/fe/bin/start_fe.sh"]
