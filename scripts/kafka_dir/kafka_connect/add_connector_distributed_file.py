import requests
import typer
import typing

def add_connect_starrocks_distributed_function(
        topics   = ['temp', 'temp2'],
        tables   = ['temp_tbl', 'temp_tbl2'], 
        name     = "starrocks-kafka-connector",
        user     = "user1", 
        passwd   = "011235813",
        database = "weather", 
        fehost   = "starrocks-fe-0"
        ):

    """
    Description: This method is used to create configuration files for kafka-starrocks-connect. 
    Created by this method file will be copied into docker container of kafka broker.   
    """
    
    if len(topics) != len(tables):
        raise Exception("Must be same number of topics and tables! ")

    allTopics = ",".join(set(topics))
    t2t = ",".join([":".join([i,j]) for i,j in zip(topics, tables)])

    configDict = {
        "connector.class":"com.starrocks.connector.kafka.StarRocksSinkConnector",
        "topics":f"{allTopics}",
        "key.converter":"org.apache.kafka.connect.json.JsonConverter",
        "value.converter":"org.apache.kafka.connect.json.JsonConverter",
        "key.converter.schemas.enable":"true",
        "value.converter.schemas.enable":"false",
        "starrocks.http.url":f"{fehost}:8030",
        "starrocks.topic2table.map":f"{t2t}",
        "starrocks.username":f"{user}",
        "starrocks.password":f"{passwd}",
        "starrocks.database.name":f"{database}",
        "sink.properties.strip_outer_array":"true",
        "errors.log.enable":"true",
        "errors.log.include.messages":"false",
        # "errors.deadletterqueue.topic.name":"my-connector-errors",
        "errors.tolerance":"all",
    }

    toSend = {
        "name":name,
        "config":configDict
    }

    url = "http://localhost:8083/connectors"

    requests.post(url, json=toSend)
    # print(toSend)

if __name__ == "__main__":

    add_connect_starrocks_distributed_function(user = "kriseu", name = "connect-0", topics=["temp"], tables=["temp_tbl"])




    # "connector.class":"com.starrocks.connector.kafka.StarRocksSinkConnector",
    # "topics":"test",
    # "key.converter":"org.apache.kafka.connect.json.JsonConverter",
    # "value.converter":"org.apache.kafka.connect.json.JsonConverter",
    # "key.converter.schemas.enable":"true",
    # "value.converter.schemas.enable":"false",
    # "starrocks.http.url":"192.168.xxx.xxx:8030",
    # "starrocks.topic2table.map":"test:test_tbl",
    # "starrocks.username":"user1",
    # "starrocks.password":"123456",
    # "starrocks.database.name":"example_db",
    # "sink.properties.strip_outer_array":"true"