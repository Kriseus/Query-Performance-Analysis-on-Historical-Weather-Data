import abc
import sqlalchemy
import pandas
import plotly.graph_objects


class abstractQuery(abc.ABC):

    @abc.abstractmethod
    def __init__(self, sqlEngine, database, table, queryMethod):
        self.sqlEngine = sqlEngine
        self.database = database
        self.table = table
        self.queryMethod = queryMethod
        self.sqlQuery = self._completeQuery()

        self.queryResult : pandas.DataFrame | None = None 

    @abc.abstractmethod
    def _completeQuery(self):
        pass

    @abc.abstractmethod
    def execute_plot(self, configs : set):
        configs = self._validatePlot(configs)
        print(configs)
        self._plot_query(configs)

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
            print(rows.keys())            
            for row in rows:
                yield row

    def to_dataframe(self):
        
        with self.sqlEngine.connect() as connection:
            connection.execute(sqlalchemy.text(f"USE {self.database};"))
            rows = connection.execute(self.sqlQuery)

        return pandas.DataFrame({key : value for key, value in zip(list(rows.keys()), zip(*rows.fetchall()))})

    def fillDataFrame(self):
        self.queryResult = self.to_dataframe()

    def to_list(self):
        return self._executeQueryResultAsList()

    def __iter__(self):

        return self._executeQueryAndReturnAsGenerator()
    
    def __call__(self):
        
        self.plot_query()

    def _validatePlot(self, configs : set):

        if self.queryResult.empty:
            raise Exception("Nothing to plot.\n")

        if configs and not (configs:= configs & set(self.queryResult.columns)):
            print("None of your configs is a viable parameter. ")
        
        if not configs:
            temporary_list = {enum: value for enum, value in enumerate([_ for _ in self.queryResult if _ not in ["latitude", "longitude", "terrain", "date"]])}
            message = "y"
            parameter = None

            if not temporary_list:
                raise Exception("There are no available columns to plot. ")

            while (message:=input("Do you wish to add plot parameter? ")) in ["y", "Y"]:
                print(f"{message}\n")
                if message not in ["y", "Y", "n", "N"]:
                    continue
                elif message in ["n, N"]:
                    break

                print("Available Params, please apply identifier(key) not value itself")
                
                for key, value in temporary_list.items():
                    print(f"{key} : {value}")
                
                while (parameter := int(input("Please apply parameter correct parameter key, not its value: "))) not in temporary_list.keys():
                    pass

                configs.add(temporary_list[parameter])
                
                if len(temporary_list.keys()) == len(configs):
                    break
            
        if configs:
            return configs
        else:
            raise Exception("configs are empty. Not possible to pass. ")
    
    def _plot_query(self, config):

        fig = plotly.graph_objects.Figure()
        config = list(config)
        vis = True
        for col in config:
            
            fig.add_trace(plotly.graph_objects.Scattermap(
            
               lat=self.queryResult["latitude"],
               lon=self.queryResult["longitude"],
               mode="markers",
               marker=dict(size=10, color=self.queryResult[col], opacity = 0.4,  colorscale="icefire", cmin=-2.5, cmax=2.5),
               name=col,
               visible=vis
               
               )
            )
            vis = False
        falses, buttons = [False] * (len(config)), []

        for enum, col in enumerate(config):
            falses_cp = falses.copy()
            falses_cp[enum] = True
            buttons.append(dict(label=col, method="update", args=[{ "visible" : falses_cp }]))

        fig.update_layout(
            map=dict(center=dict(lat=52.23, lon=21.01), zoom=3),
            updatemenus=[dict(
                buttons=buttons
            )]
        )
        
        fig.show()
    
