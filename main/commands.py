import abstract_command
import dataclasses
import app_settings

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

class CreateDatabases(abstract_command.AbstractSQLCommand):
    pass

class CreateTable(abstract_command.AbstractSQLCommand):
    pass

class CreateUsers(abstract_command.AbstractSQLCommand):
    pass

class GrantUserPrivilages(abstract_command.AbstractSQLCommand):
    pass

class StopProject(abstract_command.AbstractBashCommand): 
    pass

class StartProject(abstract_command.AbstractBashCommand):
    pass

class DownProject(abstract_command.AbstractBashCommand):
    pass

class BuildImage(abstract_command.AbstractBashCommand):
    pass


@dataclasses.dataclass(frozen = True)
class CommandBox:

    settingObj: app_settings.Settings = app_settings.Settings()

    config_connect_distributed:  ConfigConnectDistributed = ConfigConnectDistributed(settingObj)
    config_connect_standalone:  ConfigConnectStandalone = ConfigConnectStandalone(settingObj)
    produce_kafka_events:  ProduceKafkaEvents = ProduceKafkaEvents(settingObj)
    add_connect_starrocks_distributed:  AddConnectStarrocksDistributed = AddConnectStarrocksDistributed(settingObj)
    config_connect_starrocks: ConfigStarrocksSink = ConfigStarrocksSink(settingObj)
    add_topics:  AddTopics = AddTopics(settingObj)
    create_databases:  CreateDatabases = CreateDatabases(settingObj)
    create_table:  CreateTable = CreateTable(settingObj)
    create_users:  CreateUsers = CreateUsers(settingObj)
    grant_user_privilages:  GrantUserPrivilages = GrantUserPrivilages(settingObj)
    stop_project: StopProject = StopProject(settingObj)
    start_project: StartProject = StartProject(settingObj)
    down_project: DownProject = DownProject(settingObj)
    build_image: BuildImage = BuildImage(settingObj)

if __name__ == "__main__":
    import inspect 
    import importlib

    for num, tup in enumerate(inspect.getmembers(importlib.import_module(__name__))):

        if inspect.isclass(tup[1]):

            print(num, tup)