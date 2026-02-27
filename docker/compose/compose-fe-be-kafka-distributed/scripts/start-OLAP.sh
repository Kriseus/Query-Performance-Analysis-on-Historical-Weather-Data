container="starrocks-fe-0"
port="9030"
prompt="starrocks: "
host="127.0.0.1"

while [[ $# -gt 0 ]]; do
  case $1 in
    -c|--container)
      container=$2
      shift 2
      ;;
    -P|--port)
      port=$2
      shift 2
      ;;
    -p|--prompt)
      prompt=$2
      shift 2
      ;;
    -h|--host)
      host=$2
      shift 2
      ;;
  esac
done

docker compose exec $container mysql -P $port -h $host -u root --prompt="$prompt"
#docker compose exec starrocks-fe-0 mysql -P 9030 -h 127.0.0.1 -u root --prompt="StarRocks > "
