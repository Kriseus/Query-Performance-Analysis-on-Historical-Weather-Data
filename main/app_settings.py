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

<<<<<<< HEAD
        # self.functions = None  
        # self.config = None 
        self.ROOT_DIR = self.__get_directories()
        print(ROOT_DIR) 
        self.JSN_VALUES_DIR = self.ROOT_DIR / "jsons" / "parameters_values"
        self.JSN_TYPES_DIR  = self.ROOT_DIR / "jsons" / "parameters_types" 
        self.JSN_HINTS_DIR  = self.ROOT_DIR / "jsons" / "parameters_hints" 
        self.SCRIPT_DIR = self.ROOT_DIR / 'scripts'
        a, b, c, d = self.SCRIPT_DIR, self.JSN_VALUES_DIR, self.JSN_TYPES_DIR, self.JSN_HINTS_DIR
        # self.load_config()
        # self.load_functions()
        self.functions     = self.__load_functions(a)  
        # self.config        = self.__load_config(b)
        # self.types         = self.__load_config(c)
        # self.hints         = self.__load_hints(d) 
        self.methods_acces = self.__get_methods_acces()

    def __get_methods_acces(self):
=======
        self.ROOT_DIR = self.__get_directories() 
        self.JSN_DIR = self.ROOT_DIR / 'jsons'
        self.SCRIPT_DIR = self.ROOT_DIR / 'scripts'
        if str(self.SCRIPT_DIR) not in sys.path:
            sys.path.insert(str(self.SCRIPT_DIR))
        
        self.functions = self.__load_config(self.JSN_DIR)
        self.config = self.__load_config(self.SCRIPT_DIR)

    @staticmethod
    def __get_directories():
>>>>>>> thrash

        return {
                "str"   : str,                
                "bool"  : bool,
                "int"   : int,            
                "float" : float,            
                "list"  : ast.literal_eval,            
                }
    
    def __get_directories(self):
        
        DIR = pathlib.Path(__file__).resolve().parent
        while (DIR := DIR.parent).name != "Project":
            pass
        
        return DIR
    
<<<<<<< HEAD
    def __load_hints(self, dir):
        
        with open(dir / "hints.json", "r") as jsn:
            return json.loads(jsn.read()) 

    def __load_config(self, dir):

        configs = dict()
        with contextlib.chdir(dir):
            print("X kurwa d")

            for file in [_ for _ in os.listdir(dir) if _.endswith('.json')]:
                with open(file, "r") as jsn:
                    configs[file] = json.loads(jsn.read())

        return configs

    def __load_functions(self, dir):
        print(dir)

        functionsDir = dict()
        for path in map(str, pathlib.Path(self.ROOT_DIR).rglob("*")):
            if path.endswith(".py"):
                path = (
                    path
                    .removeprefix(f"{dir}/")
                    .replace("/", ".")
                    .removesuffix(".py")
                )
                print(path)
                with import_context(path) as imp:
                    functionsDir.update({name:obj for name, obj in inspect.getmembers(imp) if inspect.isfunction(obj)})

        return functionsDir


if __name__ == "__main__":

    a = Settings()
    # print(a.types)    
    pass
=======
    @staticmethod
    def __load_config(JSN_DIR):

        configs = dict()
        with contextlib.chdir(JSN_DIR):
            for file in [_ for _ in os.listdir(JSN_DIR) if _.endswith('.json')]:
                with open(file, "r") as jsn:
                    configs[file] = json.loads(jsn.read())
        return configs
    
    @staticmethod
    def __load_functions(SCRIPT_DIR):
        functionsDir = dict()
        for path in map(str, SCRIPT_DIR.rglob("*")):
            if path.endswith(".py"):
                path = (
                    path
                    .removeprefix(f"{SCRIPT_DIR}/")
                    .replace("/", ".")
                    .removesuffix(".py")
                )

                with contextlib.chdir(SCRIPT_DIR):
                    with import_context(path) as imp:
                        functionsDir.update({name:obj for name, obj in inspect.getmembers(imp) if inspect.isfunction(obj)})

        return functionsDir

if __name__ == "__main__":
    
    a = Settings()
    print(a.functions)
>>>>>>> thrash
