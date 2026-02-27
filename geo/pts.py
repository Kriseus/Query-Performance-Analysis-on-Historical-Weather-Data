from continents import Europe

def squaresGenerator(continentClass, diff = 10):

    currW, currH = continentClass.__dict__["extremes"]["west"], continentClass.__dict__["extremes"]["south"]
    while currW < continentClass.__dict__["extremes"]["east"]:         
        while currH < continentClass.__dict__["extremes"]["north"]:
            yield {"minLong":currW, "maxLong":currW+diff, "minLat" :currH, "maxLat":currH+diff}
            currH += diff
        
        currH = continentClass.__dict__["extremes"]["south"]
        currW += diff


if __name__ == "__main__":

    europa = Europe()
    [print(d) for d in squaresGenerator(europa)]