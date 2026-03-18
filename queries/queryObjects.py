import abstractQuery
import queryMethods

class Query3(abstractQuery.abstractQuery):
    def __init__(self, 
                sqlEngine,
                database, table,
                mainYear ='2021', 
                comparisonYears = ['2012', '2013', '2014'], 
                parameter = "T2M", 
                limit = 100):

        self.mainYear = mainYear  
        self.comparisonYears = comparisonYears  
        self.parameter = parameter  
        self.limit = limit

        super().__init__(sqlEngine = sqlEngine, database = database, table = table, queryMethod = queryMethods.method_query_3,)
        
    def _completeQuery(self):
        return self.queryMethod(self.table, self.mainYear, self.comparisonYears, self.parameter, self.limit,)

    def execute_plot(self, configs = None):
        raise Exception("Nothing to plot. ")

class Query4(abstractQuery.abstractQuery):
 
    def __init__(self, sqlEngine, 
                database, 
                table,
                mainYear ='2021', comparisonYears = ['2012', '2013', '2014'], 
                parameter = "T2M", limit = 100,
                ):
    
        self.mainYear = mainYear
        self.comparisonYears = comparisonYears
        self.parameter = parameter
        self.limit = limit

        super().__init__(sqlEngine, database, table, queryMethod = queryMethods.method_query_4)

    def _completeQuery(self):
        return self.queryMethod(self.table, self.mainYear, self.comparisonYears, self.parameter, self.limit )
    
    def execute_plot(self, configs = None):
        raise Exception("Nothing to plot. ")

class Query5(abstractQuery.abstractQuery):
    
    def __init__(self, sqlEngine, 
                database = 'weather', 
                table = "temperatures_table",
                mainYear ='2021', comparisonYears = ['2019', '2017', '1986'], 
                parameter = "T2M", limit = 1000000000,
                ):
    
        self.mainYear = mainYear
        self.comparisonYears = comparisonYears
        self.parameter = parameter
        self.limit = limit


        super().__init__(sqlEngine, database, table, queryMethod = queryMethods.method_query_5)

    def _completeQuery(self):
        return self.queryMethod(self.table, self.mainYear, self.comparisonYears, self.parameter, self.limit )
    

    def execute_plot(self, configs):
        return super().execute_plot(configs = configs)

if __name__ == "__main__":
    
    import sqlalchemy

    engine = sqlalchemy.create_engine('starrocks://root@localhost:9030/')
    que = Query5(engine, limit = 10000000000)

    que.fill_DataFrame()
    print(que.queryResult.to_string())
    que.execute_plot({
        "AVG_T2M_2021_2017",
        "AVG_T2M_2021_2019",
        "AVG_T2M_2021_1986",
        }
        )
    # config = {}
    # que.execute_plot()