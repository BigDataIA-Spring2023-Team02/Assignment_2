import os
import sqlite3
import pandas as pd
from pathlib import Path
from scrape_metadata import *

class GoesSqlite:
    def __init__(self):

        database_file_name = 'scrape_data.db'
        self.database_file_path = os.path.join(os.path.dirname(__file__), database_file_name)
        ddl_file_name = 'geos18.sql'
        self.ddl_file_path = os.path.join(os.path.dirname(__file__), ddl_file_name)
        
        scrape_metadata = Scrape_Data()
        self.df = scrape_metadata.geos18_data()
        self.df.to_csv('geos18_data.csv', index = False, na_rep = 'Unknown', encoding = 'utf-8')
        self.table_name = 'GEOS18'
    
    def create_database(self):
        with open(self.ddl_file_path, 'r') as sql_file:
            sql_script = sql_file.read()        
        db = sqlite3.connect(self.database_file_path)
        self.df.to_sql(self.table_name, db, if_exists = 'replace', index=False)
        cursor = db.cursor()
        cursor.executescript(sql_script)
        db.commit()
        db.close()

    def check_database_initilization(self):
        print(os.path.dirname(__file__))
        if Path(self.database_file_path).is_file():
            self.create_database()
        else:
            raise SystemExit

    def fetch_from_sql_into_df(self):
        db = sqlite3.connect(self.database_file_path)
        df1 = pd.read_sql_query("SELECT * FROM GEOS18", db)
        return df1

    def main(self):
        self.check_database_initilization()
        data = self.fetch_from_sql_into_df()
        return data

class NexradSqlite:
    def __init__(self):

        database_file_name = 'scrape_data.db'
        self.database_file_path = os.path.join(os.path.dirname(__file__), database_file_name)
        ddl_file_name = 'nexrad.sql'
        self.ddl_file_path = os.path.join(os.path.dirname(__file__), ddl_file_name)

        scrape_metadata = Scrape_Data()
        self.df = scrape_metadata.nexrad_data()
        self.df.to_csv('nexrad_data.csv', index = False, na_rep = 'Unknown', encoding = 'utf-8')
        self.table_name = 'NEXRAD'

    def create_database(self):
        with open(self.ddl_file_path, 'r') as sql_file:
            sql_script = sql_file.read()        
        db = sqlite3.connect(self.database_file_path)
        self.df.to_sql(self.table_name, db, if_exists = 'replace', index=False)
        cursor = db.cursor()
        cursor.executescript(sql_script)
        db.commit()
        db.close()

    def check_database_initilization(self):
        print(os.path.dirname(__file__))
        if Path(self.database_file_path).is_file():
            self.create_database()
        else:
            raise SystemExit

    def fetch_from_sql_into_df(self):
        db = sqlite3.connect(self.database_file_path)
        df1 = pd.read_sql_query("SELECT * FROM NEXRAD", db)
        return df1

    def main(self):
        self.check_database_initilization()
        data = self.fetch_from_sql_into_df()
        return data

class NexradMapSqlite:
    def __init__(self):

        database_file_name = 'scrape_data.db'
        self.database_file_path = os.path.join(os.path.dirname(__file__), database_file_name)
        ddl_file_name = 'nexradmap.sql'
        self.ddl_file_path = os.path.join(os.path.dirname(__file__), ddl_file_name)

        scrape_metadata = Scrape_Data()
        self.df = scrape_metadata.nexradmap_data()
        self.df.to_csv('nexradmap_data.csv', index = False, na_rep = 'Unknown', encoding = 'utf-8')
        self.table_name = 'NexradMap'

    def create_database(self):
        with open(self.ddl_file_path, 'r') as sql_file:
            sql_script = sql_file.read()        
        db = sqlite3.connect(self.database_file_path)
        self.df.to_sql(self.table_name, db, if_exists = 'replace', index=False)
        cursor = db.cursor()
        cursor.executescript(sql_script)
        db.commit()
        db.close()

    def check_database_initilization(self):
        print(os.path.dirname(__file__))
        if Path(self.database_file_path).is_file():
            self.create_database()
        else:
            raise SystemExit

    def fetch_from_sql_into_df(self):
        db = sqlite3.connect(self.database_file_path)
        df1 = pd.read_sql_query("SELECT * from NexradMap", db)
        return df1

    def main(self):
        self.check_database_initilization()
        data = self.fetch_from_sql_into_df()
        return data

class UserSqlite:
    def __init__(self):

        database_file_name = 'scrape_data.db'
        self.database_file_path = os.path.join(os.path.dirname(__file__), database_file_name)
        ddl_file_name = 'users.sql'
        self.ddl_file_path = os.path.join(os.path.dirname(__file__), ddl_file_name)
        
        scrape_metadata = Scrape_Data()
        self.df = scrape_metadata.geos18_data()
        self.table_name = 'Users'
    
    def create_database(self):
        with open(self.ddl_file_path, 'r') as sql_file:
            sql_script = sql_file.read()        
        db = sqlite3.connect(self.database_file_path)
        self.df.to_sql(self.table_name, db, if_exists = 'replace', index=False)
        cursor = db.cursor()
        cursor.executescript(sql_script)
        db.commit()
        db.close()

    def check_database_initilization(self):
        print(os.path.dirname(__file__))
        if Path(self.database_file_path).is_file():
            self.create_database()
        else:
            raise SystemExit

    def fetch_from_sql_into_df(self):
        db = sqlite3.connect(self.database_file_path)
        df1 = pd.read_sql_query("SELECT * FROM Users", db)
        return df1

    def main(self):
        self.check_database_initilization()
        data = self.fetch_from_sql_into_df()
        return data

def main():
    geos_sql = GoesSqlite()
    nexrad_sql = NexradSqlite()
    nexradmap_sql = NexradMapSqlite()
    user_sql = UserSqlite()

    geos_sql.main()
    nexrad_sql.main()
    nexradmap_sql.main()
    user_sql.main()

if __name__ == "__main__":
    main()