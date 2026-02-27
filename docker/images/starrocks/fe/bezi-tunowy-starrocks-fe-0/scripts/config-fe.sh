#!/bin/bash

num=1

while getopts "n:" opt; do
  case $opt in
    n)
      num="$OPTARG"
      ;;
  esac
done



echo -e "meta_dir = /opt/starrocks/fe/metadata \npriority_networks = 172.18.0.0/16 \ndefault_replication_num = $num" >> /opt/starrocks/fe/conf/fe.conf