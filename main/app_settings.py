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

        self.functions = None  
        self.config = None 
        self.ROOT_DIR = self._get_directories() 
        self.JSN_DIR = self.ROOT_DIR / 'jsons'
        self.SCRIPT_DIR = self.ROOT_DIR / 'scripts'
        self.load_config()
        self.load_functions()

    @staticmethod
    def _get_directories():

        DIR = pathlib.Path(__file__).resolve().parent
        while DIR.name != "Project":
            DIR = DIR.parent

        return DIR

    def load_config(self):

        configs = dict()
        with contextlib.chdir(self.JSN_DIR):
            for file in [_ for _ in os.listdir(self.JSN_DIR) if _.endswith('.json')]:
                with open(file, "r") as jsn:
                    configs[file] = json.loads(jsn.read())

        self.config = configs

    def load_functions(self):

        functionsDir = dict()
        for path in map(str, pathlib.Path(self.SCRIPT_DIR).rglob("*")):
            if path.endswith(".py"):
                path = (
                    path
                    .removeprefix(f"{self.SCRIPT_DIR}/")
                    .replace("/", ".")
                    .removesuffix(".py")
                )

                with import_context(path) as imp:
                    functionsDir.update({name:obj for name, obj in inspect.getmembers(imp) if inspect.isfunction(obj)})

        self.functions = functionsDir

if __name__ == "__main__":
    
    pass