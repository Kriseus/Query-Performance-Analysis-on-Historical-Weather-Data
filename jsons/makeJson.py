#!/home/bezi-tunowy/Bezi-Tunowy/Project/.projectVenv/bin/python3
import json
import re

# def rebuildJson(filename):
    
    # filename


class test:
    def func(self):

        a = f"{__class__}"
        r = (re.findall(r"'(.*?)'", f"{self.__class__}")[0]).split(".")[1]    

        print(r)
    def retName(self):
        return __name__

if __name__ == "__main__":

    jsonName = "config_connect_distributed.json"
    jsonDict = {
        "kafhost" : "justTestingIfItWorks",
        "path" : "/home/bezi-tunowy/Bezi-Tunowy/Project/docker/images/kafka/distributed-connector/config",
        }


    with open(jsonName, "w") as jsn:

        jsn.write(json.dumps(jsonDict))

    # print(test().__class__.__name__)

    # a = ""
    # with open("is_initialized.json", "r") as jsn:
    #     a = json.loads(jsn.read())
    # print(a)
    # print(type(a))

    # a = test()
    # a.func()
    # print(dir(int))