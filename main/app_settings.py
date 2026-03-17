import sys
import contextlib
import importlib
import pathlib
import os
import json 
import inspect
import ast
import sqlalchemy

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
        # self.QUERIES_DIR = self.ROOT_DIR / "queries"    
        self.JSN_QUERY_VALUES_DIR = self.ROOT_DIR / 'jsons' / "query_values"    
        self.JSN_QUERY_TYPES_DIR = self.ROOT_DIR  / 'jsons' / "query_types"    

        if str(self.SCRIPT_DIR) not in sys.path:
            sys.path.insert(1, str(self.SCRIPT_DIR))
        
        self.functions = self.__load_functions(self.SCRIPT_DIR)
        self.bash_scripts = self.__load_bash_scripts(self.SCRIPT_DIR)
        self.config = self.__load_jsns(self.JSN_VALUES_DIR)
        self.types = self.__load_jsns(self.JSN_TYPES_DIR) 
        self.hints = self.__load_hints(self.JSN_HINTS_DIR)
        self.query_config = self.__load_jsns(self.JSN_QUERY_VALUES_DIR) 
        self.query_types = self.__load_jsns(self.JSN_QUERY_TYPES_DIR) 

        self.methods_acces = self.__get_methods()

        self.sqlEngine = sqlalchemy.create_engine('starrocks://root@localhost:9030/')

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
    
    @staticmethod
    def __load_bash_scripts(dir):
        scriptsDict = dict()
        name = ""
        for path in dir.rglob("*"):
            if (name:=path.name).endswith(".sh"):
                scriptsDict[name.removesuffix(".sh")] = str(path)

        return scriptsDict 

    def reload_functions(self):
        self.functions = self.__load_functions(self.SCRIPT_DIR)

    def reload_configs(self):
        self.config = self.__load_jsns(self.JSN_VALUES_DIR)       