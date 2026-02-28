import contextlib
import os
import sys
import requests
import json 
import datetime
import csv
import io  
import pathlib

import shapely
import geopandas
 
ROOT_DIR = pathlib.Path(__file__).resolve().parent
while (ROOT_DIR := ROOT_DIR.parent).name != "Project":
    pass

GEO_DIR, SHP_DIR = ROOT_DIR / "geo", ROOT_DIR / "data" / "countries"
SHP_FILENAME = "ne_10m_admin_0_countries.shp"

if GEO_DIR.exists():
    sys.path.insert(1, str(GEO_DIR))
else:   
    raise FileNotFoundError(f"Your Geo directory ({str(GEO_DIR)}) does not exist. Make sure You downoladaed proejcet correctly.")

if not (SHP_DIR / SHP_FILENAME).exists():
    raise ValueError(f""" Your shp file does not exists, has not correct FILENAME ({str(SHP_FILENAME)}) or not correct PATH ({str(SHP_DIR)}). 
                     Make sure that you initialized you project first or uploaded changes correctly. """)

import continents

class JsonGenerator:

    def __init__(self, APIparameters, spaceTimeDictionary, continentInstance):
        self.__listOfGenerators = [self.__NASAPowerRegionalCSVRequestGenerator(i, spaceTimeDictionary) for i in APIparameters] 
        self.__continentMultiPolygon = continentInstance.ContinentShape

    @staticmethod
    def __formattedRowGenerator(reader, parameterName):
        """ 
        INPUT ROWS: 0-LAT 1-LON 2-YEAR 3-DAY_OF_THE_YEAR (DOY) 4-PARAMETER
        """    
        for row in reader: 
            formattedRow = dict()
            formattedRow["latitude"] = row[0]
            formattedRow["longitude"] = row[1]
            formattedRow["date"] = (datetime.datetime(int(row[2]), 1, 1) + datetime.timedelta(days=int(row[3]) - 1)).strftime("%Y-%m-%d")
            formattedRow[parameterName] = row[4]
            yield formattedRow

    def __NASAPowerRegionalCSVRequestGenerator(self, parameter, spaceTimeDictionary):
        req = requests.get(f"https://power.larc.nasa.gov/api/temporal/daily/regional?start={spaceTimeDictionary["timeStart"]}&end={spaceTimeDictionary["timeEnd"]}&latitude-min={spaceTimeDictionary["minLat"]}&latitude-max={spaceTimeDictionary["maxLat"]}&longitude-min={spaceTimeDictionary["minLong"]}&longitude-max={spaceTimeDictionary["maxLong"]}&community=ag&parameters={parameter}&format=csv&header=false")
        csvReader = csv.reader(io.StringIO(req.text), delimiter=',')
        next(csvReader)
        
        return self.__formattedRowGenerator(csvReader, parameter)

    def __landOrSea(self, point, jsn):
        if self.__continentMultiPolygon.contains(point):
            jsn["terrain"] = "land"
        else:
            jsn["terrain"] = "sea"

    def __iter__(self):
        for generation in zip(*self.__listOfGenerators):
            futureJson = {}
            for j in generation:
                futureJson.update(j)

            futureJson = dict(futureJson)
            self.__landOrSea(shapely.Point(futureJson["longitude"], futureJson["latitude"]), futureJson)
            yield json.dumps(futureJson)

if __name__ == "__main__":
    with contextlib.chdir(SHP_DIR):
        worldDataFrame = geopandas.read_file(SHP_FILENAME)

    APIparameters = ["T2M", "T10M"]
    spaceTimeDictionary = {
        "timeStart":"20200101",
        "timeEnd":"20200105",
        "minLat":41,
        "maxLat":46,
        "minLong":-4,
        "maxLong":-2
    }

    europe = continents.Europe(worldDataFrame)
    jsnGen = JsonGenerator(APIparameters=APIparameters, spaceTimeDictionary=spaceTimeDictionary, continentInstance=europe)

    for i in jsnGen:
        print(i)