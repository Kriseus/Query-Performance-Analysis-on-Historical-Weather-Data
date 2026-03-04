import pathlib
import sys 
import functools
import geopandas
import multiprocessing
import inspect

ROOT_DIR = pathlib.Path(__file__).resolve().parent

while (ROOT_DIR := ROOT_DIR.parent).name != "Project":
    pass

PRODUCER_DIR, GEO_DIR, SHP_DIR = ROOT_DIR / "producer", ROOT_DIR / "geo", ROOT_DIR / "data" / "countries" 
SHP_FILENAME = "ne_10m_admin_0_countries.shp"

sys.path.insert(1, str(PRODUCER_DIR))
sys.path.insert(1, str(GEO_DIR))

import Producer
import pts
import continents 

def produce_kafka_events_function(
            continentName="Europe",
            bootstrap="localhost:9094",            
            timeStart= 20140101,
            timeEnd=20140131,           
            APIparameters = ["T2M", "T10M"],
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
    
    Producer.produceSmallEvents( 
        areaList[0],
        config = configDict, 
        kafkaTopic = kafTopic, 
        timeDictionary = timeDictionary, 
        APIparameters = APIparameters, continentInstance = continentInstance
        )


if __name__ == "__main__":

    produce_kafka_events_function(kafTopic = "temperatures")