import confluent_kafka.admin
import typer
import typing 

def add_topics_function(
        kafTopic = ["temperatures"], # typing.List[str] | None = typer.Option(["temperatures"], "--topic", "-t"), 
        bootstrap = "localhost:9094"): #: str | None = typer.Option("localhost:9094", "--bootstrap", "-b")):

    config = {"bootstrap.servers":bootstrap}
    kafAdmin = confluent_kafka.admin.AdminClient(config)
    # t = confluent_kafka.admin.NewTopic(kafTopic)
    topics = [confluent_kafka.admin.NewTopic(name) for name in kafTopic]
    kafAdmin.create_topics(topics)


if __name__ == "__main__":

    add_topics_function(kafTopic = ["temp"])