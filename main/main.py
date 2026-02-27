#!/usr/bin/env python3

import commands
import app_settings

import cmd2
import sys
import pathlib


class Main(cmd2.Cmd):

    def __init__(self):

        super().__init__()
        self.settingsObj = app_settings.Settings()

    def do_goodbye_mars(self, _: cmd2.Statement):
        print("Goodbye Mars")

    def do_config_distributed(self, _: cmd2.Statement):
        commands.ConfigConnectDistributed(self.settingsObj).cmdloop()

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