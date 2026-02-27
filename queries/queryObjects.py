import abstractQuery
import queryMethods

class Query3(abstractQuery.abstractQuery):

    def __init__(self, sqlEngine, database, table, queryMethod = queryMethods.method_query_3,
                 mainYear ='2021', comparisonYears = {'2012', '2013', '2014'}, 
                 parameter = "T2M", limit = 100):

        self.mainYear = mainYear  
        self.comparisonYears = comparisonYears  
        self.parameter = parameter  
        self.limit = limit

        super().__init__(sqlEngine = sqlEngine, database = database, table = table, queryMethod = queryMethod)

        
    def _completeQuery(self):
        
        return self.queryMethod(self.table, self.mainYear, self.comparisonYears, self.parameter, self.limit,)
    
class Query4(abstractQuery.abstractQuery):
    
    def __init__(self, sqlEngine, database, table, queryMethod = queryMethods.method_query_4, 
                 mainYear ='2021', comparisonYears = {'2012', '2013', '2014'}, 
                 parameter = "T2M", limit = 100,
                 ):
        self.mainYear = mainYear
        self.comparisonYears = comparisonYears
        self.parameter = parameter
        self.limit = limit

        super().__init__(sqlEngine, database, table, queryMethod)

    def _completeQuery(self):
        return self.queryMethod(self.table, self.mainYear, self.comparisonYears, self.parameter, self.limit )
    
if __name__ == "__main__":
    
    pass