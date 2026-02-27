import abc
import sqlalchemy

class abstractQuery(abc.ABC):

    @abc.abstractmethod
    def __init__(self, sqlEngine, database, table, queryMethod):

        self.sqlEngine = sqlEngine
        self.database = database
        self.table = table
        self.queryMethod = queryMethod
        self.sqlQuery = self._completeQuery()

    @abc.abstractmethod
    def _completeQuery(self):
        pass

    def showQuery(self):
        print(self.sqlQuery)
    
    def returnQuery(self):
        return self.sqlQuery
    
    def executeQuery(self):
        with self.sqlEngine.connect() as connection:

            connection.execute(sqlalchemy.text(f"USE {self.database};"))
            connection.execute(self.sqlQuery)

    def _executeQueryResultAsList(self):
        with self.sqlEngine.connect() as connection:

            connection.execute(sqlalchemy.text(f"USE {self.database};"))
            rows = connection.execute(self.sqlQuery).fetchall()
        
        return rows
    
    def _executeQueryAndReturnAsGenerator(self):
        with self.sqlEngine.connect() as connection:

            connection.execute(sqlalchemy.text(f"USE {self.database};"))
            rows = connection.execute(self.sqlQuery)
            
            for row in rows:
                yield row

    def to_list(self):
        
        return self._executeQueryResultAsList()

    def __iter__(self):

        return self._executeQueryAndReturnAsGenerator()