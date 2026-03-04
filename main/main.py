#!/usr/bin/env python3

import commands

import cmd2
import sys
import pathlib

class Main(cmd2.Cmd):

    def __init__(self):
        super().__init__()
        self.all_commands: commands.CommandBox = commands.CommandBox()

    def do_goodbye_mars(self, _: cmd2.Statement):
        print("Goodbye Mars")

    def do_config_distributed(self, _: cmd2.Statement):
        sys.exit(self.all_commands.config_connect_distributed.cmdloop())

    def do_config_standalone(self, _: cmd2.Statement):
        sys.exit(self.all_commands.config_connect_standalone.cmdloop())

    def do_produce_kafka_events(self, _: cmd2.Statement):
        sys.exit(self.all_commands.produce_kafka_events.cmdloop())

    def do_add_connect_starrocks_distributed(self, _: cmd2.Statement):
        sys.exit(self.all_commands.add_connect_starrocks_distributed.cmdloop())

    def do_config_connect_starrocks(self, _: cmd2.Statement):
        sys.exit(self.all_commands.config_connect_starrocks)

    def do_add_topics(self, _: cmd2.Statement):
        sys.exit(self.all_commands.add_topics.cmdloop())

    def do_create_databases(self, _: cmd2.Statement):
        sys.exit(self.all_commands.create_databases)

    def do_create_table(self, _: cmd2.Statement):
        sys.exit(self.all_commands.create_table.cmdloop())

    def do_create_users(self, _: cmd2.Statement):
        sys.exit(self.all_commands.create_users.cmdloop())

    def do_grant_user_privilages(self, _: cmd2.Statement):
        sys.exit(self.all_commands.grant_user_privilages.cmdloop())



if __name__ == '__main__':


    FILE_DIR = pathlib.Path(__file__).resolve().parent
    ROOT_DIR = FILE_DIR

    while ROOT_DIR.name != "Project":
        ROOT_DIR = ROOT_DIR.parent

    JSN_DIR = ROOT_DIR / "jsons"
    SCRIPT_DIR = ROOT_DIR / "scripts"

    sys.path.insert(1, str(SCRIPT_DIR))

    main = Main()
    sys.exit(main.cmdloop())