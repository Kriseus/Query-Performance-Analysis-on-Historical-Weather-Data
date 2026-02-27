import typer
import typing
import pathlib

FILE_DIR = pathlib.Path(__file__).resolve().parent
ROOT_DIR = FILE_DIR

while ROOT_DIR.name != "Project":
    ROOT_DIR = ROOT_DIR.parent

def config_connect_starrocks_function(
        topics: typing.List[str] | None = typer.Option(['temp', 'temp2'], "--topic", "-t"),
        tables: typing.List[str] | None = typer.Option(['temp_tbl', 'temp_tbl2'], "--table", "-T"),
        name: str | None = typer.Option("starrocks-kafka-connector", "--name", "-n"),
        user: str | None = typer.Option("user1", "--user", "-u"),
        passwd: str | None = typer.Option("011235813", "--passwd", "-p"),
        database: str | None = typer.Option("weather", "--dtb", "-d"),
        fehost: str | None = typer.Option("starrocks-fe", "--host", "-f"),
        path: str | None = typer.Option(ROOT_DIR / "docker/images/bezi-tunowy-kafka-0/config", "--path", "-P") 
        ):

    if len(topics) != len(tables):
        raise Exception("Must be same number of topics and tables! ")

    allTopics = ",".join(set(topics))
    t2t = ",".join([":".join([i,j]) for i,j in zip(topics, tables)])

    configString = [
        f"name={name}",
        f"connector.class=com.starrocks.connector.kafka.StarRocksSinkConnector",
        f"topics={allTopics}",
        f"key.converter=org.apache.kafka.connect.json.JsonConverter",
        f"value.converter=org.apache.kafka.connect.json.JsonConverter",
        f"key.converter.schemas.enable=true",
        f"value.converter.schemas.enable=false",
        f"starrocks.http.url={fehost}:8030",
        f"starrocks.topic2table.map={t2t}",
        f"starrocks.username={user}",
        f"starrocks.password={passwd}",
        f"starrocks.database.name={database}",
        f"sink.properties.strip_outer_array=true",
        ]
    
    with open( pathlib.Path(path) / "connect-starrocks-sink.properties", "w" ) as starrocks:
        
        starrocks.write("\n".join(configString))

    return




    # topics: typing.List[str] | None = typer.Option(['temp', 'temp2'], "--topic", "-t"),
    # tables: typing.List[str] | None = typer.Option(['temp_tbl', 'temp_tbl2'], "--table", "-T"),
    # name: str | None = typer.Option("starrocks-kafka-connector", "--name", "-n"),
    # user: str | None = typer.Option("user1", "--user", "-u"),
    # passwd: str | None = typer.Option("011235813", "--passwd", "-p"),
    # database: str | None = typer.Option("weather", "--dtb", "-d"),
    # fehost: str | None = typer.Option("starrocks-fe", "--host", "-f"),
    # path: str | None = typer.Option("/home/bezi-tunowy/Bezi-Tunowy/Project/docker/images/bezi-tunowy-kafka-0/config", "--path", "-P")
