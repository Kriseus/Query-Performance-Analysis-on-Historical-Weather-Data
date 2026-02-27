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

        self.all_configs:typing.Dict[ str, typing.Dict[str, typing.Any] ]  = settingObj.config
        self.all_functions: typing.Dict[str, typing.Callable ]= settingObj.functions
        self.JSN_DIR: pathlib.Path = settingObj.JSN_DIR
        self.SCRIPT_DIR: pathlib.Path = settingObj.SCRIPT_DIR 
        self.me: str = self.get_name()
        self.my_config_key: str = f"{self.me}.json"
        self.my_function_key: str = f"{self.me}_function"

    def get_name(self):

        return re.sub(r'(?<!^)(?=[A-Z])', '_', self.__class__.__name__).lower()    
    
    def do_rebuild_Json(self, _: cmd2.Statement):

        enumertor = { iter : key for iter, key in enumerate(self.all_configs[self.my_config_key].keys())}
        updatedDict  = self.all_configs[self.my_config_key].copy()
        
        input_cont = "Do You wish to change parameter? y/n :\n"
        input_key = "Please select one of the following, numbers which matches the key you are intrested in " + f"{enumertor}" + " :\n"
        input_value = "Please apply value of the parameter you chose :\n"
        
        while (cont:= input(input_cont)) not in ("N", "n"):
            
            if cont not in ("y","Y"):
                continue
            
            while (key:=int(input(input_key))) not in enumertor.keys():
                pass

            value = input(input_value)
            updatedDict[enumertor[key]] = value
            
        with open( self.JSN_DIR / self.my_config_key, "w") as jsn:

            jsn.write(json.dumps(updatedDict))

    def do_reloadJson(self, _: cmd2.Statement):

        with open(self.JSN_DIR / self.my_config_key, "r") as jsn:
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
        f"{self.JSN_DIR}\n",
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