import abc
import cmd2
import re
import pathlib
import json
import typing 
import functools
import subprocess

ROOT_DIR = pathlib.Path(__file__).resolve().parent
while (ROOT_DIR := ROOT_DIR.parent).name != "Project":
    pass

JSN_DIR = ROOT_DIR / "jsons"

""" << ZEROTH ABSTRACTION LAYER >> """

class AbstractBase(abc.ABC, cmd2.Cmd):
    def __init__(self, settingObj):
        super().__init__()

        self.settings_alias = settingObj

        """Configs"""

        self.all_configs: typing.Dict[ str, typing.Dict[ str, typing.Any ] ]
        self.all_types: typing.Dict[ str, str ]

        """Local keys"""
        self.my_config_key: str

        """Directories"""
        self.JSN_VALUES_DIR: pathlib.Path
        
        """Hints"""
        self.my_types: typing.Dict[ str, str ]
        self.my_hints: typing.Dict[ str, str ] = self.settings_alias.hints

        """Input Hints"""
        self.enumerator_over_config_keys: typing.Dict[ int, str ]
        self.input_messages: typing.Dict[ str, str ]= {
            "input_cont"  : "Do You wish to change parameter? y/n :\n",
            "input_key"   : "Please select one of the following, numbers which matches the key you are intrested in " + f"{self.enumerator_over_config_keys}" + " :\n",
            "input_value" : "Please apply value of the parameter you chose :\n"
        }

        """Methods Acces"""
        self.methods_acces : typing.Dict[str, typing.Callable] = self.settings_alias.methods_acces
        
        """Prompt"""
        self.prompt:str = f" << {self.__class__.__name__} >> : "
    
    @property
    def me(self):
        # return re.sub(r'(?<!^)(?=[A-Z])', '_', self.__class__.__name__).lower() 
        return re.sub(r'(?<!^)(?=[A-Z0-9])', '_', self.__class__.__name__).lower()   
    
    @property
    def my_config_key(self)->str:
        return f"{self.me}.json"
    

    @property
    def enumerator_over_config_keys(self):
        return { iter : key for iter, key in enumerate(self.all_configs[self.my_config_key].keys())}
    
    @property
    @abc.abstractmethod
    def my_types(self)->typing.Dict[ str, str ]:
        return 

    @property
    @abc.abstractmethod
    def JSN_VALUES_DIR(self) -> pathlib.Path:
        return
    
    @property
    @abc.abstractmethod
    def all_configs(self) -> typing.Dict[ str, typing.Dict[str, typing.Any] ]:
        return
    
    @property
    @abc.abstractmethod
    def all_types(self) -> typing.Dict[str, str ]:
        return

    def __show_configs(self):
        print("<<ALL CONFIG VARIABLES>>")
        for key, value in self.all_configs[self.my_config_key].items():
            print(f"Parameter: {key}: {value}")

    def __get_updates(self):
        self.__show_configs()
        updated_dict  = self.all_configs[self.my_config_key].copy()
        while (cont:= input(self.input_messages["input_cont"])) not in ("N", "n"):

            if cont not in ("y","Y"):
                continue

            while (key:=int(input(self.input_messages["input_key"]))) not in self.enumerator_over_config_keys.keys():
                pass

            key_method = self.methods_acces[self.my_types[self.enumerator_over_config_keys[key]]]
            print(self.my_hints[self.my_types[self.enumerator_over_config_keys[key]]])
            value = key_method(input(f"{self.input_messages["input_value"]}"))
            if str(input("Do You wish to show current configs? ")) in ('Y', 'y'):
                self.__show_configs()

            updated_dict[self.enumerator_over_config_keys[key]] = value
        
        return updated_dict
    
    def do_rebuild_Json(self, _: cmd2.Statement):
        updated_dict = self.__get_updates() 
        with open( self.JSN_VALUES_DIR / self.my_config_key, "w") as jsn:
            jsn.write(json.dumps(updated_dict))

    def do_reloadJson(self, _: cmd2.Statement):
        with open(self.JSN_VALUES_DIR / self.my_config_key, "r") as jsn:
            self.all_configs[self.my_config_key] = json.loads(jsn.read())
    
    def do_rebuild_and_reload(self, _: cmd2.Statement):
        self.do_rebuild_Json(self)
        self.do_reloadJson(self)

    def do_show_current_config(self, _: cmd2.Statement):
        self.__show_configs()

    @abc.abstractmethod
    def do_execute(self, _: cmd2.Statement):
        pass

""" << FIRST ABSTRACTION LAYER >> """

class AbstractCommand(AbstractBase):
    def __init__(self, settingObj):
        super().__init__(settingObj)

    @property
    def my_types(self)->typing.Dict[ str, str ]:
        return self.settings_alias.types[ self.my_config_key ]


    @property
    def JSN_VALUES_DIR(self) -> pathlib.Path:
        return self.settings_alias.JSN_VALUES_DIR
            
    @property
    def all_configs(self) -> typing.Dict[ str, typing.Dict[str, typing.Any] ]:
        return self.settings_alias.config
    
    @property
    def all_types(self) -> typing.Dict[str, str ]:
        return self.settings_alias.types

class AbstractQueryCommand(AbstractBase):

    plot_paraser = cmd2.Cmd2ArgumentParser()
    plot_paraser.add_argument("configs", type=str, nargs="*")
    
    def __init__(self, settingObj, queryClass):
        super().__init__(settingObj)

        self.sqlEngine = settingObj.sqlEngine
        self.QueryClass = queryClass
        self.QueryInstance = self.QueryClass(self.sqlEngine, **self.all_configs[self.my_config_key])
    @property
    def my_types(self) -> typing.Dict[ str, str ]:
        return self.settings_alias.query_types[ self.my_config_key ]

    @property
    def JSN_VALUES_DIR(self) -> pathlib.Path:
        return self.settings_alias.JSN_QUERY_VALUES_DIR
            
    @property
    def all_configs(self) -> typing.Dict[ str, typing.Dict[str, typing.Any] ]:
        return self.settings_alias.query_config
    
    @property
    def all_types(self) -> typing.Dict[str, str ]:
        return self.settings_alias.query_types
    
    def do_show_params(self, _: cmd2.Statement):
        for k, v in self.__dict__.items():
            print(k, v)
    
    def do_show_query(self, _: cmd2.Statement):
        self.QueryInstance.showQuery()

    def do_execute(self, _: cmd2.Statement):
        self.QueryInstance.executeQuery()

    def do_show_res(self, _:cmd2.Statement):
        print(self.QueryInstance.queryResult)

    def do_fill_dataframe(self, _: cmd2.Statement):
        self.QueryInstance.fill_DataFrame()
        print(self.QueryInstance.queryResult)
        
    @cmd2.with_argparser(plot_paraser)
    def do_plot_query(self, args):
        configs = set(args.configs.copy())
        self.QueryInstance.fill_DataFrame()
        self.QueryInstance.execute_plot(configs)

""" << SECOND ABSTRACTION LAYER >> """

class AbstractPythonCommand(AbstractCommand):
    def __init__(self, settingObj):
        super().__init__(settingObj)

        """Configs"""
        self.all_functions: typing.Dict[str, typing.Callable ] = self.settings_alias.functions
        
        """Local keys"""
        self.my_function_key: str = f"{self.me}_function"

    def do_execute(self, _: cmd2.Statement):
        self.all_functions[self.my_function_key](**self.all_configs[self.my_config_key])

class AbstractBashCommand(AbstractCommand):
    def __init__(self, settingObj):
        super().__init__(settingObj)

        """Configs"""
        self.all_bash_scripts: typing.Dict[str, str] = settingObj.bash_scripts

        """Local keys"""
        self.my_scripts_key: str = f"{self.me}"

    def do_execute(self, _: cmd2.Statement):
        subprocess.Popen( 
            ["/bin/bash", self.all_bash_scripts[self.my_scripts_key]],  
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

class AbstractSQLCommand(AbstractCommand):

    def __init__(self, settingObj):
        
        super().__init__(settingObj)
        
        """Configs"""
        self.all_functions: typing.Dict[str, typing.Callable ] = settingObj.functions

        """Local keys"""
        self.my_function_key: str = f"{self.me}_function"
        self.sqlEngine = settingObj.sqlEngine

    def do_execute(self, _: cmd2.Statement):
        ready_to_exec = functools.partial(self.all_functions[self.my_function_key], **self.all_configs[self.my_config_key])
        ready_to_exec(self.sqlEngine)  

""" << END OF ABSTRACTION >> """