import sqlalchemy

def create_databases_function(sqlEngine, databases = ["weather"]):
    
    with sqlEngine.connect() as connection:

        for i in databases:

            connection.execute(sqlalchemy.text(f"""CREATE DATABASE IF NOT EXISTS {i};"""))


def create_table_function(sqlEngine, database = "weather", name = "temp_tbl", 
                 parameterColumns = ["T2M", "T10M"],
                 types = ["FLOAT", "FLOAT"]):

    if len(parameterColumns) != len(types):
        raise ValueError


    firstQueryPart = [f"CREATE TABLE IF NOT EXISTS {name} (","date DATE,","latitude DECIMAL(5,3),","longitude DECIMAL(6,3),"]
    secondQueryPart = [f"{col} {typ} MAX," for col, typ in zip(parameterColumns, types)]
    thirdQueryPart = ["terrain STRING MIN)", "AGGREGATE KEY(date, latitude, longitude)", "PARTITION BY date_trunc('YEAR', date)", "DISTRIBUTED BY HASH(date);"]
                        
    query = sqlalchemy.text("\n".join(firstQueryPart + secondQueryPart + thirdQueryPart))

    with sqlEngine.connect() as connection:

        connection.execute(sqlalchemy.text(f"USE {database};"))
        connection.execute(query)

    return

def create_users_function(sqlEngine, usernames = ["kriseu"], passwds = ["011235813"]):

    if len(usernames)!=len(passwds):
        raise ValueError

    with sqlEngine.connect() as connection:

        for username, passwd in zip(usernames, passwds):

            connection.execute(sqlalchemy.text(f"CREATE USER IF NOT EXISTS '{username}' IDENTIFIED BY '{passwd}';"))

    return

def grant_user_privilages_function(sqlEngine, username = 'kriseu', privileges = ["ALL"], table = "ALL TABLES", database = "ALL DATABASES"):

    """ AVAILABLE PRIVILAGES: ALTER | DROP | SELECT | INSERT | EXPORT | UPDATE | DELETE | ALL """

    with sqlEngine.connect() as connection:

        connection.execute(sqlalchemy.text(f"GRANT {",".join(privileges)} ON {table} IN {database} TO USER {username}"))
    
    return


if __name__ == "__main__":

    starrocks = sqlalchemy.create_engine('starrocks://root@localhost:9030/')
