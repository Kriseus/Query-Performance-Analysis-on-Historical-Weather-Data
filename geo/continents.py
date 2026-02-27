import shapely
import geopandas
import pandas
import abc 
import matplotlib.pyplot

class Continent(abc.ABC):
    def __init__(self, worldDataFrame, name, northPoint, southPoint, eastPoint, westPoint, transcontinentalCountires):

        rightUp = shapely.Point(eastPoint, northPoint)
        leftUp = shapely.Point(westPoint, northPoint)
        rightdown = shapely.Point(eastPoint, southPoint)
        leftDown = shapely.Point(westPoint,southPoint)
        
        self.name = name
        self.worldDataFrame = worldDataFrame

        self.extremes = {'north' : northPoint, 'south' : southPoint, 'west' : westPoint, 'east' : eastPoint }
        self.borders = shapely.Polygon([leftUp, rightUp, rightdown, leftDown])
        self.transcontinentalCountires = transcontinentalCountires

        self.ContinentShape = self._completeContintent()

    def _completeContintent(self):

        polygonsIter = list(self.worldDataFrame.query(f'CONTINENT == "{self.name}"')['geometry']) + list((self.worldDataFrame.merge(pandas.DataFrame({"NAME_EN":self.transcontinentalCountires}), on = "NAME_EN", ))["geometry"])
        polygons = []

        for i in polygonsIter:
            if type(i)==shapely.MultiPolygon:
                for j in list(i.geoms):
                    polygons.append(j)
            else:
                polygons.append(i)

        return shapely.MultiPolygon(polygons)


    def plot(self, color = 'green'):
        ax=matplotlib.pyplot.axes()
        ax.set_xlim(self.extremes['west'], self.extremes['east'])
        ax.set_ylim(self.extremes['south'], self.extremes['north'])
        self.worldDataFrame.plot(color=color, ax=ax, marker="*")
        # shapely.plotting.plot_polygon(self.ContinentShape, color = "green", linewidth=1)

    def __eq__(self,other):
        return type(self) == type(other) 


class Europe(Continent):

    def __init__(self, worldDataFrame, name = "Europe", northPoint = 82, southPoint = 34, eastPoint = 59, westPoint = -32):
        
        transcontinentalCountires = [
            'Azerbaijan',
            'Georgia',
            'Kazakhstan',
            'Turkey',
            'Cyprus'
        ]

        super().__init__(
            worldDataFrame = worldDataFrame, 
            name = name, 
            northPoint = northPoint,
            southPoint = southPoint, 
            eastPoint = eastPoint, 
            westPoint = westPoint, 
            transcontinentalCountires = transcontinentalCountires
        )

        
if __name__ == '__main__':


    print(locals())

    worldDataFrame = geopandas.read_file("/home/bezi-tunowy/Bezi-Tunowy/Project/data/countries")

    europa = Europe(worldDataFrame)

    europa.plot()


    matplotlib.pyplot.show()



