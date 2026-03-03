import abc
import cmd2
import re
import pathlib
import json
import typing 

FILE_DIR = pathlib.Path(__file__).resolve().parent
ROOT_DIR = FILE_DIR

while ROOT_DIR.name != "Project":
    ROOT_DIR = ROOT_DIR.parent
JSN_DIR = ROOT_DIR / "jsons"

class AbstractCommand(abc.ABC, cmd2.Cmd):

    def __init__(self, settingObj):
        
        super().__init__()

        """Configs"""
        self.all_configs: typing.Dict[ str, typing.Dict[str, typing.Any] ] = settingObj.config
        self.all_functions: typing.Dict[str, typing.Callable ] = settingObj.functions
        self.all_types: typing.Dict[str, str ] = settingObj.types

        """Directories"""
        self.SCRIPT_DIR: pathlib.Path = settingObj.SCRIPT_DIR
        self.JSN_VALUES_DIR: pathlib.Path = settingObj.JSN_VALUES_DIR
        self.JSN_HINTS_DIR: pathlib.Path = settingObj.JSN_HINTS_DIR
        self.JSN_TYPES_DIR: pathlib.Path = settingObj.JSN_TYPES_DIR
        
        """Identification"""
        self.me: str = self.__get_name()
        
        """Local keys"""
        self.my_config_key: str = f"{self.me}.json"
        self.my_function_key: str = f"{self.me}_function"

        """Hints"""
        self.my_hints: typing.Dict[ str, str ] = settingObj.hints
        self.my_types: typing.Dict[ str, str ] = settingObj.types[ self.my_config_key ]

        """Input Hints"""
        self.enumerator_over_config_keys: typing.Dict[ int, str ] = self.__get_enumerator_over_config_keys()
        self.input_messages: typing.Dict[ str, str ]= {
            "input_cont"  : "Do You wish to change parameter? y/n :\n",
            "input_key"   : "Please select one of the following, numbers which matches the key you are intrested in " + f"{self.enumerator_over_config_keys}" + " :\n",
            "input_value" : "Please apply value of the parameter you chose :\n"
        }

        """Methods Acces"""
        self.methods_acces : typing.Dict[str, typing.Callable] = settingObj.methods_acces

    def __get_name(self):

        return re.sub(r'(?<!^)(?=[A-Z])', '_', self.__class__.__name__).lower()    
    
    def __get_enumerator_over_config_keys(self):
        return { iter : key for iter, key in enumerate(self.all_configs[self.my_config_key].keys())}
    
    def __get_updates(self):

        updated_dict  = self.all_configs[self.my_config_key].copy()
        
        while (cont:= input(self.input_messages["input_cont"])) not in ("N", "n"):
            if cont not in ("y","Y"):
                continue
            while (key:=int(input(self.input_messages["input_key"]))) not in self.enumerator_over_config_keys.keys():
                pass

            key_method = self.methods_acces[self.my_types[self.enumerator_over_config_keys[key]]]
            
            value = key_method(input(  f"{self.input_messages["input_value"]}"))
            print(type(value), " : " ,value)
            # updated_dict[self.enumerator_over_config_keys[key]] = value
        
        # return updated_dict
    
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

    def do_execute(self, _: cmd2.Statement):
        
        self.all_functions[self.my_function_key](**self.all_configs[self.my_config_key])

    def do_show(self, _: cmd2.Statement):

        print(
        f"{self.all_configs}\n",
        f"{self.all_functions}\n",
        f"{self.JSN_VALUES_DIR}\n",
        f"{self.SCRIPT_DIR}\n",
        f"{self.me}\n",
        f"{self.my_config_key}\n",
        f"{self.my_function_key}\n",
        )

if __name__ == "__main__":

    enum = {
        1:"path",
        2:"name",
        3:"passwd",
        4:"topic",
        5:"table",
    }
    
    while (cont:= input("Do You wish to change parameter? y/n ")) not in ("N", "n"):
            if cont not in ("y","Y"):
                print("Thats not correct value...")
                continue
            
            while (key:=input("Please select one of the following, numbers which matches the key you are intrested in:\n" + str(enum))) not in map(str,enum.keys()):
                pass

            value = str(input("Please apply value of the parameter you chose: "))