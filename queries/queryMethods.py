import sys
import inspect
import sqlalchemy

def method_query_0(table = "temp_tbl", date = '2021-01-05', terrain = 'land', parameter = 'T2M', than = 5, order = 'DESC', by = '1, 2, 3'):
    sqlQuery = sqlalchemy.text("\n".join([
        f"SELECT * FROM {table}", 
        f"WHERE date='{date}' AND terrain LIKE '{terrain}' AND {parameter} > {than} ",
        f"ORDER BY {by} {order}"
        ])
        )
    return sqlQuery

def method_query_1(date0 = '2021-01-01', date1 = '2021-01-02', terrain = 'land', order = "1 DESC, 2 ASC", limit = 25, database = 'weather'):    
    sqlQuery = sqlalchemy.text("\n".join([
        f"SELECT latitude, longitude,",
        f"ROUND(SUM(CASE WHEN date = '{date0}' AND terrain = '{terrain}' THEN T2M END), 2) AS firstDate,",
        f"ROUND(SUM(CASE WHEN date = '{date1}' AND terrain = '{terrain}' THEN T2M END), 2) AS secondDate,",
        f"ROUND(firstDate - secondDate, 2)",
        f"FROM temp_tbl  GROUP BY latitude, longitude ",
        f"HAVING firstDate IS NOT NULL AND secondDate IS NOT NULL  ",
        f"ORDER BY {order} LIMIT {limit};",
        ]))

    return sqlQuery

def method_query_2(date = '2021-01-02', table = 'temp_tbl'):
    return sqlalchemy.text(f"SELECT latitude, longitude, CASE WHEN date = {date} THEN date ELSE NULL FROM {table} ORDER BY 1 LIMIT 100")

def method_query_3( table = 'temp_tbl', 
                    mainYear = '2021', 
                    comparisonYears = {'2012', '2013', '2014'}, 
                    parameter = 'T2M', 
                    limit = 100,
                    ):

    def buildPivotColumn(year, parameter = parameter):
        return f"ROUND(SUM(CASE WHEN YEAR(date) = '{year}' THEN {parameter} END), 2) AS YEAR_{year}"
    
    def buildDiffColumn(year, mainYear = mainYear, parameter = parameter):
        return f"ROUND(YEAR_{mainYear} - YEAR_{year}, 2) AS '{parameter}_{mainYear}_{year}'"

    def buildHavingLine(year):
        return f"YEAR_{year} IS NOT NULL"

    def applyPivotColumns(years = comparisonYears, mainYear = mainYear):
        helpList = ([(buildPivotColumn(year), buildDiffColumn(year), buildHavingLine(year)) for year in years])

        colsList, diffList, havingList = zip(*helpList)
        colsString = ",\n".join([ buildPivotColumn(mainYear), *colsList, *diffList])
        havingString = "HAVING " + " AND\n".join([buildHavingLine(mainYear), *havingList])

        return colsString, havingString
    
    cols, having = applyPivotColumns()
    
    sqlQuery = "\n".join(
    [
        "SELECT latitude, longitude, MONTH(date) AS month, DAY(date) day,", 
        cols, 
        f"FROM {table}",
        f"GROUP BY  latitude, longitude, month, day", 
        having, 
        f"LIMIT {limit};"
    ])
    
    return sqlalchemy.text(sqlQuery)

def method_query_4( table = 'temp_tbl', 
            mainYear = '2021', 
            comparisonYears = {'2012', '2013', '2014'}, 
            parameter = 'T2M', 
            limit = 100,
            ):
    
    if mainYear in comparisonYears:
        comparisonYears = comparisonYears - mainYear
    # if len(comparisonYears) == 0:
    #     raise ValueError
    if not comparisonYears:
        raise ValueError
    def buildJoinColumns(year, parameter = parameter):
        return f"""(SELECT latitude, longitude, date, {parameter} AS {parameter}{year} FROM {table} WHERE YEAR(date) = '{year}') AS sub_{year}"""

    def buildConditions(year, mainYear = mainYear, parameter = parameter):
        firstPart = [f"sub_{mainYear}.{p} = sub_{year}.{p}" for p in ["latitude", "longitude"]]
        secondPart = [f"{p}(sub_{mainYear}.date) = {p}(sub_{year}.date)" for p in ["DAY", "MONTH"]]

        return " ON "+ " AND ".join(firstPart + secondPart)

    def buildSelect(mainYear = mainYear, comparisonYears = comparisonYears, parameter = parameter):
        firstPart = f"SELECT sub_{mainYear}.latitude, sub_{mainYear}.longitude, MONTH(sub_{mainYear}.date), DAY(sub_{mainYear}.date), {parameter}{mainYear}, "
        secondPart, thirdPart = zip(*[(f"{parameter}{year}",f"{parameter}{mainYear}-{parameter}{year}") for year in comparisonYears])

        return firstPart + ", ".join(secondPart + thirdPart)
    
    def applyJoinColumns(comparisonYears = comparisonYears, mainYear = mainYear, parameter = parameter):
            
        return "\n".join(["JOIN" + buildJoinColumns(year) + buildConditions(year) for year in comparisonYears])

    sqlQuery = "\n".join(
    [
        buildSelect(),
        "FROM "+buildJoinColumns(mainYear),
        applyJoinColumns(),
        f"LIMIT {limit};"
    ])
    
    return sqlalchemy.text(sqlQuery)

def query5():

    pass

def query6():

    pass

if __name__ == "__main__":
    
    module = sys.modules[__name__]

    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj):
            print("FUNKCJA:", name)
        elif inspect.isclass(obj):
            print("KLASA:", name)