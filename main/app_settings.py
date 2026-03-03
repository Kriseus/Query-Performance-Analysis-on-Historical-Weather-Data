import sys 
import contextlib
import importlib
import pathlib
import os 
import json 
import inspect
import ast  

ROOT_DIR = pathlib.Path(__file__).resolve().parent

while (ROOT_DIR := ROOT_DIR.parent).name != "Project":
    pass

@contextlib.contextmanager
def import_context(module):
    yield importlib.import_module(module)

class Settings:
    def __init__(self):

        self.ROOT_DIR = self.__get_directories() 
        self.JSN_VALUES_DIR = self.ROOT_DIR / 'jsons' / "parameters_values"
        self.JSN_TYPES_DIR = self.ROOT_DIR / 'jsons' / "parameters_types" 
        self.JSN_HINTS_DIR = self.ROOT_DIR / 'jsons' / "parameters_hints" 
        self.SCRIPT_DIR = self.ROOT_DIR / 'scripts'
        
        if str(self.SCRIPT_DIR) not in sys.path:
            sys.path.insert(1, str(self.SCRIPT_DIR))
        
        self.functions = self.__load_functions(self.SCRIPT_DIR)
        self.config = self.__load_jsns(self.JSN_VALUES_DIR)
        self.types = self.__load_jsns(self.JSN_TYPES_DIR) 
        self.hints = self.__load_hints(self.JSN_HINTS_DIR)
        self.methods_acces = self.__get_methods()
    @staticmethod
    def __get_methods():

        return {
                "str"   : str,                
                "bool"  : bool,
                "int"   : int,            
                "float" : float,            
                "list"  : ast.literal_eval,            
                }
    
    @staticmethod
    def __get_directories():
        
        DIR = pathlib.Path(__file__).resolve().parent
        while (DIR := DIR.parent).name != "Project":
            pass
        
        return DIR
    
    @staticmethod
    def __load_hints(dir):
        
        with open(dir / "hints.json", "r") as jsn:
            return json.loads(jsn.read()) 

    @staticmethod
    def __load_jsns(dir):
        configs = dict()

        with contextlib.chdir(dir):
            for file in [_ for _ in os.listdir(str(dir)) if _.endswith('.json')]:
                with open(file, "r") as jsn:
                    configs[file] = json.loads(jsn.read())

        return configs
    
    @staticmethod
    def __load_functions(dir):

        functionsDir = dict()
        for path in map(str, dir.rglob("*")):
            if path.endswith(".py"):
                path = (
                    path
                    .removeprefix(f"{dir}/")
                    .replace("/", ".")
                    .removesuffix(".py")
                )
                with import_context(path) as imp:
                    functionsDir.update({name:obj for name, obj in inspect.getmembers(imp) if inspect.isfunction(obj)})

        return functionsDir
    
    def reload_functions(self):
        self.functions = self.__load_functions(self.SCRIPT_DIR)

    def reload_configs(self):
        self.config = self.__load_jsns(self.JSN_VALUES_DIR)
         

if __name__ == "__main__":

    a = Settings()
    print(a.functions)
    print(a.hints)
    print(a.types)
    print(a.config)
