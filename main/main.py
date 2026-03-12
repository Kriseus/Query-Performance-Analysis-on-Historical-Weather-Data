#!/usr/bin/env python3

import commands

import cmd2
import sys
import pathlib

class Main(cmd2.Cmd):

    def __init__(self):
        super().__init__()
        self.prompt : str = f"<<{self.__class__.__name__}>> : " 
        self.all_commands: commands.CommandBox = commands.CommandBox()
    
    @cmd2.with_category("Useless")
    def do_goodbye_mars(self, _: cmd2.Statement):
        print("Goodbye Mars")
    
    @cmd2.with_category("Config")
    def do_config_distributed(self, _: cmd2.Statement):
        self.all_commands.config_connect_distributed.cmdloop()
    
    @cmd2.with_category("Config")
    def do_config_standalone(self, _: cmd2.Statement):
        self.all_commands.config_connect_standalone.cmdloop()

    @cmd2.with_category("Kafka")
    def do_produce_kafka_events(self, _: cmd2.Statement):
        self.all_commands.produce_kafka_events.cmdloop()

    @cmd2.with_category("Kafka")
    def do_add_connect_starrocks_distributed(self, _: cmd2.Statement):
        self.all_commands.add_connect_starrocks_distributed.cmdloop()

    @cmd2.with_category("Kafka")
    def do_config_connect_starrocks(self, _: cmd2.Statement):
        self.all_commands.config_connect_starrocks.cmdloop()

    @cmd2.with_category("Kafka")
    def do_add_topics(self, _: cmd2.Statement):
        self.all_commands.add_topics.cmdloop()

    @cmd2.with_category("Starrocks")
    def do_create_databases(self, _: cmd2.Statement):
        self.all_commands.create_databases.cmdloop()

    @cmd2.with_category("Starrocks")
    def do_create_table(self, _: cmd2.Statement):
        self.all_commands.create_table.cmdloop()

    @cmd2.with_category("Starrocks")
    def do_create_users(self, _: cmd2.Statement):
        self.all_commands.create_users.cmdloop()

    @cmd2.with_category("Starrocks")
    def do_grant_user_privilages(self, _: cmd2.Statement):
        self.all_commands.grant_user_privilages.cmdloop()

    @cmd2.with_category("Starrocks")
    def do_start_project(self, _: cmd2.Statement):
        self.all_commands.start_project.cmdloop()

    @cmd2.with_category("Project")
    def do_stop_project(self, _: cmd2.Statement):
        self.all_commands.stop_project.cmdloop()
    
    @cmd2.with_category("Project")
    def do_down_project(self, _: cmd2.Statement):
        self.all_commands.down_project.cmdloop()

    @cmd2.with_category("Project")
    def do_build_image(self, _: cmd2.Statement):
        self.all_commands.build_image.cmdloop()
        
    @cmd2.with_category("Starrocks")
    def do_query_3(self, _:cmd2.Statement):
        self.all_commands.query_3.cmdloop()





if __name__ == '__main__':
    ROOT_DIR = pathlib.Path(__file__).resolve().parent

    while (ROOT_DIR := ROOT_DIR.parent).name != "Project":
        pass

    JSN_DIR = ROOT_DIR / "jsons"
    SCRIPT_DIR = ROOT_DIR / "scripts"

    # sys.path.insert(1, str(SCRIPT_DIR))

    main = Main()
    sys.exit(main.cmdloop())