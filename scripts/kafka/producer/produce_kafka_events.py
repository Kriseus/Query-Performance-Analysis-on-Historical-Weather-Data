# TODO: This file is not finished yet.

import pathlib
import sys 
import functools
import geopandas
import multiprocessing
import inspect

FILE_DIR = pathlib.Path(__file__).resolve().parent
ROOT_DIR = FILE_DIR

while str(ROOT_DIR)[-7:] != "Project":
    ROOT_DIR = ROOT_DIR.parent

PRODUCER_DIR = ROOT_DIR / "producer" 
GEO_DIR = ROOT_DIR / "geo"
SHP_DIR = ROOT_DIR / "data" / "countries"
SHP_FILENAME = "ne_10m_admin_0_countries.shp"

sys.path.insert(1, str(PRODUCER_DIR))
sys.path.insert(1, str(GEO_DIR))

import Producer
import pts
import continents 

def produce_events_function(
            continentName="Europe",
            bootstrap="localhost:9094",            
            timeStart= 20140101,
            timeEnd=20141231,           
            APIparameters = ["T2M, T10M"],
            kafTopic="temperatures", 
            multipocesses = 12
            ):

    configDict = {"bootstrap.servers":bootstrap}
    timeDictionary = {"timeStart": timeStart, "timeEnd" : timeEnd}
    worldDataFrame = geopandas.read_file(SHP_DIR / SHP_FILENAME)
    continentInstance = dict(inspect.getmembers(continents, inspect.isclass))[continentName](worldDataFrame)
    areaList = [_ for _ in pts.squaresGenerator(continentInstance)]

    multiProducer = functools.partial(
        Producer.produceSmallEvents, config = configDict, 
        kafkaTopic = kafTopic, 
        timeDictionary = timeDictionary, 
        APIparameters = APIparameters, continentInstance = continentInstance
    )

    with multiprocessing.Pool(multipocesses) as pool:
        
        pool.map(multiProducer, areaList)


if __name__ == "__main__":

    produce_events_function(kafTopic = "temp")