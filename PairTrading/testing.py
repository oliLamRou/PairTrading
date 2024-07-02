import configparser

from PairTrading.src.utils import PROJECT_ROOT
from PairTrading.src import _constant


class DataBase:
    def __init__(self, path):
        self._conn = None
        self._cursor = None
        self.path = path


class Polygon():
    def __init__(self):        
        #API_KEY
        self.config = configparser.ConfigParser()
        self.config.read(_constant.CONFIG)
        self.key = self.config['polygon']['API_KEY']

class Data(Polygon, DataBase):
    DB = (PROJECT_ROOT / 'data' / 'polygon.db').resolve()

    def __init__(self):
        Polygon.__init__(self)
        DataBase.__init__(self, path = self.DB)
        


d = Data()
print(d.key)


import sqlite3

# Connect to the SQLite database (replace 'example.db' with your database file)
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Define the table name, column name, and value to check
table_name = 'new_table'
column_name = 'ticker'
value_to_check = 'DNN'

def table_exists(cursor, table_name):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    return cursor.fetchone() is not None

# Function to check if a table exists
def table_exists(cursor, table_name):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    return cursor.fetchone() is not None

# Check if the table exists
if table_exists(cursor, table_name):
    print(f"Table '{table_name}' exists. Executing the SELECT query...")

    # Execute the SELECT query with the specified condition
    cursor.execute(f'SELECT * FROM "{table_name}" WHERE "{column_name}" = ?', (value_to_check,))
    
    # Fetch all results
    rows = cursor.fetchall()
    
    # Check if any rows were returned
    if rows:
        print(f"Rows matching {column_name} = {value_to_check}:")
        for row in rows:
            print(row)
    else:
        print(f"No rows found matching {column_name} = {value_to_check}.")
else:
    print(f"Table '{table_name}' does not exist.")

# Close the connection
conn.close()
