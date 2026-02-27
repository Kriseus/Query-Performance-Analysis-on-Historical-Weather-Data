#TODO: file is not ready yet

import json
import subprocess
import pathlib

FILE_DIR = pathlib.Path(__file__).resolve().parent

ROOT_DIR = FILE_DIR
while ROOT_DIR.name != "Project":
    ROOT_DIR = ROOT_DIR.parent

JSN_DIR = ROOT_DIR / "jsons"
INIT_FILENAME = "is-initialized.json"

def checkStatus():
    
    with open( JSN_DIR / INIT_FILENAME, "r") as jsn:

        if json.loads(jsn.read())["IS_INITIALIZED"]:

            raise Exception("Project is already initialized! ")
    

INIT_DIR = ROOT_DIR / "scripts" / "initialization" / "initialize_once"


def initialize():
    
    checkStatus()
    a = [file for file in INIT_DIR.iterdir()]
    a.sort()
    for file in a:
        
        if file.is_file():
    
            subprocess.run([file])
    
if __name__=="__main__":

    pass