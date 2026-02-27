import os
import sys
import pathlib
import json
import uuid
import time
import confluent_kafka
import geopandas
import multiprocessing
import functools

FILE_DIR = pathlib.Path(__file__).resolve().parent
ROOT_DIR = FILE_DIR.parent

while str(ROOT_DIR)[-7:] != "Project":
    ROOT_DIR = ROOT_DIR.parent

GEO_DIR = ROOT_DIR / "geo"
SHP_DIR = ROOT_DIR / "data" / "countries"
SHP_FILENAME = "ne_10m_admin_0_countries.shp"
# print(GEO_DIR)

if GEO_DIR.exists():
    sys.path.insert(1, str(GEO_DIR))
else:
    raise FileExistsError("Your Geo directory does not exist. Make sure you initialize project correctly.")

import jsonGenerator
import pts
import continents

def produceFullEvents(config, kafkaTopic, areaGenerator, timeDictionary, APIparameters, continentInstance):
    
    fullProducer = confluent_kafka.Producer(config)

    for area in areaGenerator:

        spacetimeDictionary = timeDictionary.copy() | area

        for jsn in jsonGenerator.JsonGenerator(APIparameters, spacetimeDictionary, continentInstance):
        
            fullProducer.produce(topic = kafkaTopic, value = jsn.encode("utf-16"))
            fullProducer.flush()

def produceSmallEvents(area, config, kafkaTopic, timeDictionary, APIparameters, continentInstance):

    smallProducer = confluent_kafka.Producer(config)

    spacetimeDictionary = timeDictionary.copy() | area

    for jsn in jsonGenerator.JsonGenerator(APIparameters, spacetimeDictionary, continentInstance):
        
        smallProducer.produce(topic = kafkaTopic, value = jsn.encode("utf-16"))
        smallProducer.flush() 

if __name__ == "__main__":

    os.chdir(SHP_DIR)
    worldDataFrame = geopandas.read_file(SHP_FILENAME)
    os.chdir(FILE_DIR)

    timeDictionary = {"timeStart": 20140101, "timeEnd": 20140131}
    APIparameters = ["T2M", "T10M"]
    configDict = {"bootstrap.servers":"localhost:9094"}
    europe = continents.Europe(worldDataFrame)
    topic = "temp"
    areaGenerator = pts.squaresGenerator(europe)

    multiProducer = functools.partial(produceSmallEvents, config = configDict, kafkaTopic = topic, timeDictionary = timeDictionary, APIparameters = APIparameters, continentInstance = europe)

    with multiprocessing.Pool(12) as pool:
        pool.map(multiProducer, [i for i in areaGenerator])
