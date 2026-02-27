#!/bin/bash

basic_path = "/home/bezi-tunowy/Bezi-Tunowy/Project/docker/compose/"
directory = "compose-fe-be-kafka"

while [[ $# -gt 0 ]]; do
  case "$1" in
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

docker compose -f "$basic_path$directory" start
