import abstract_command



class ConfigConnectDistributed(abstract_command.AbstractCommand):
    pass

class ConfigConnectStandalone(abstract_command.AbstractCommand):
    pass

class ProduceKafkaEvents(abstract_command.AbstractCommand):
    pass

class AddConnectStarrocksDistributed(abstract_command.AbstractCommand):
    pass

class ConfigConnectStarrocks(abstract_command.AbstractCommand):
    pass

class AddTopics(abstract_command.AbstractCommand):
    pass

class CreateDatabases(abstract_command.AbstractCommand):
    pass

class CreateTable(abstract_command.AbstractCommand):
    pass

class CreateUsers(abstract_command.AbstractCommand):
    pass

class GrantUserPrivilages(abstract_command.AbstractCommand):
    pass

    


if __name__ == "__main__":
    import inspect 
    import importlib

    for num, tup in enumerate(inspect.getmembers(importlib.import_module(__name__))):

        if inspect.isclass(tup[1]):

            print(num, tup)