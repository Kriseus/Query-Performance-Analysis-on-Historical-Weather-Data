import sys 
import contextlib
import importlib
import pathlib
import os 
import json 
import inspect

FILE_DIR = pathlib.Path(__file__).resolve().parent
ROOT_DIR = FILE_DIR

while ROOT_DIR.name != "Project":
    ROOT_DIR = ROOT_DIR.parent

@contextlib.contextmanager
def import_context(module):
    yield importlib.import_module(module)

class Settings:
    def __init__(self):

        self.ROOT_DIR = self.__get_directories() 
        self.JSN_DIR = self.ROOT_DIR / 'jsons'
        self.SCRIPT_DIR = self.ROOT_DIR / 'scripts'
        if str(self.SCRIPT_DIR) not in sys.path:
            sys.path.insert(str(self.SCRIPT_DIR))
        
        self.functions = self.__load_config(self.JSN_DIR)
        self.config = self.__load_config(self.SCRIPT_DIR)

    @staticmethod
    def __get_directories():

        DIR = pathlib.Path(__file__).resolve().parent
        while DIR.name != "Project":
            DIR = DIR.parent

        return DIR
    
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