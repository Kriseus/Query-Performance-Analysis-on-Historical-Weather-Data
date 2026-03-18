import abstract_command
import dataclasses
import app_settings
import pathlib
import sys

ROOT_DIR = pathlib.Path(__file__).resolve()

while (ROOT_DIR := ROOT_DIR.parent).name != "Project":
    pass

sys.path.insert(1, str(ROOT_DIR / "queries"))

import queryObjects

""" << Python Commands >> """

class ConfigConnectDistributed(abstract_command.AbstractPythonCommand):
    pass

class ConfigConnectStandalone(abstract_command.AbstractPythonCommand):
    pass

class ProduceKafkaEvents(abstract_command.AbstractPythonCommand):
    pass

class AddConnectStarrocksDistributed(abstract_command.AbstractPythonCommand):
    pass

class ConfigStarrocksSink(abstract_command.AbstractPythonCommand):
    pass

class AddTopics(abstract_command.AbstractPythonCommand):
    pass

""" << SQL Commands >> """

class CreateDatabases(abstract_command.AbstractSQLCommand):
    pass

class CreateTable(abstract_command.AbstractSQLCommand):
    pass

class CreateUsers(abstract_command.AbstractSQLCommand):
    pass

class GrantUserPrivilages(abstract_command.AbstractSQLCommand):
    pass

""" << Bash Scripts Commands >> """

class StopProject(abstract_command.AbstractBashCommand): 
    pass

class StartProject(abstract_command.AbstractBashCommand):
    pass

class DownProject(abstract_command.AbstractBashCommand):
    pass

class BuildImage(abstract_command.AbstractBashCommand):
    pass

""" << SQL Queries Commands >> """

class QueryCommand3(abstract_command.AbstractQueryCommand):
    def __init__(self, settingObj, queryClass = queryObjects.Query3):
        super().__init__(settingObj, queryClass)

class QueryCommand4(abstract_command.AbstractQueryCommand):
    def __init__(self, settingObj, queryClass = queryObjects.Query4):
        super().__init__(settingObj, queryClass)

class QueryCommand5(abstract_command.AbstractQueryCommand):
    def __init__(self, settingObj, queryClass = queryObjects.Query5):
        super().__init__(settingObj, queryClass)

""" << Command Box >> """

@dataclasses.dataclass(frozen = True)
class CommandBox:

    settingObj: app_settings.Settings = app_settings.Settings()

    config_connect_distributed        : ConfigConnectDistributed = ConfigConnectDistributed(settingObj)
    config_connect_standalone         : ConfigConnectStandalone = ConfigConnectStandalone(settingObj)
    produce_kafka_events              : ProduceKafkaEvents = ProduceKafkaEvents(settingObj)
    add_connect_starrocks_distributed : AddConnectStarrocksDistributed = AddConnectStarrocksDistributed(settingObj)
    config_connect_starrocks          : ConfigStarrocksSink = ConfigStarrocksSink(settingObj)
    add_topics                        : AddTopics = AddTopics(settingObj)
    create_databases                  : CreateDatabases = CreateDatabases(settingObj)
    create_table                      : CreateTable = CreateTable(settingObj)
    create_users                      : CreateUsers = CreateUsers(settingObj)
    grant_user_privilages             : GrantUserPrivilages = GrantUserPrivilages(settingObj)
    stop_project                      : StopProject = StopProject(settingObj)
    start_project                     : StartProject = StartProject(settingObj)
    down_project                      : DownProject = DownProject(settingObj)
    build_image                       : BuildImage = BuildImage(settingObj)
    query_3                           : QueryCommand3 = QueryCommand3(settingObj)
    query_4                           : QueryCommand3 = QueryCommand3(settingObj)
    query_5                           : QueryCommand5 = QueryCommand5(settingObj)

if __name__ == "__main__":

    box = CommandBox()

    que = box.query_3
    que.do_rebuild_and_reload(None)