#!/bin/bash

basic_path = "/home/bezi-tunowy/Bezi-Tunowy/Project/docker/images/"
directory = "bezi-tunowy-kafka-0"
name = "kafka-0"
user = "bezi-tunowy/"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -n|--name)
      name="$2"
      shift 2
      ;;
    -u|--user)
      user="$2"
      shift 2
      ;;  
    -p|--path)
      basic_path="$2"
      shift 2
      ;;
    -d|--dir)
      directory="$2"
      shift 2
      ;;  
    -h|--help)
      echo -e "--path -p: path to docker compose target file. "
      exit
      ;;
  esac
done

docker build -t "$user$name" "$basic_path$directory"
