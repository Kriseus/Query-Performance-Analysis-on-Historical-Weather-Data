import pathlib
import pathlib
import typer
import json


FILE_DIR = pathlib.Path(__file__).resolve().parent
ROOT_DIR = FILE_DIR
while ROOT_DIR.name != "Project":
    ROOT_DIR = ROOT_DIR.parent

def config_connect_standalone_function(
        kafhost: str | None = typer.Option("kafka-0", "--kafhost", "-k"),
        path:    str | None = typer.Option(ROOT_DIR / "docker/images/kafka/distributed-connector/bezi-tunowy-kafka-0/config", "--path", "-p"),
        ):
    
    configString = [
        f"bootstrap.servers={kafhost}:9092",
        f"offset.storage.file.filename=/tmp/connect.offsets",
        f"offset.flush.interval.ms=10000",
        f"key.converter=org.apache.kafka.connect.json.JsonConverter",
        f"value.converter=org.apache.kafka.connect.json.JsonConverter",
        f"key.converter.schemas.enable=true",
        f"value.converter.schemas.enable=false",
        f"plugin.path=/home/appuser/connector/starrocks-kafka-connector-1.0.4"
        ]

    with open( pathlib.Path(path) / f"connect-standalone.properties", "w" ) as standalone:
        
        standalone.write("\n".join(configString))

if __name__ == "__main__":

    
    with open(ROOT_DIR / "jsons" /"config_connect_distributed.json", "r") as jsn:    
        config = json.loads(jsn.read())
