import sqlite3
import pandas as pd

class DataBase:
    def __init__(self, path):
        self._conn = None
        self._cursor = None
        self.path = path

    @property
    def conn(self):
        if not self._conn:
            self._conn = sqlite3.connect(self.path)

        return self._conn

    @property
    def cursor(self):
        if not self._cursor:
            self._cursor = self.conn.cursor()

        return self._cursor

    def list_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        print(self.cursor.fetchall())

    def list_table_columns(self, table_name) -> list:
        self.cursor.execute(f'''PRAGMA table_info({table_name})''')
        columns = [col[1] for col in self.cursor.fetchall()]
        print(columns)
        return columns

    def list_table_data(self, table_name):
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", self.conn)
        print(df)

    def create_table(self, table_name):
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY)'''
        )

    def add_columns(self, 
            table_name: str, 
            columns: dict
        ):
        
        current_columns = self.list_table_columns(table_name)
        for column_name, column_type in columns.items():
            if column_name in current_columns:
                continue

            self.cursor.execute(f'''ALTER TABLE {table_name} ADD {column_name} {column_type}''') 
        
        self.conn.commit()
        self.list_table_columns(table_name)
        
    def add_row(self, table_name: str, row: dict):
        columns = tuple(row.keys())
        values = tuple(row.values())
        self.cursor.execute(f"INSERT INTO {table_name} {columns} VALUES {values}")        
        self.conn.commit()

if __name__ == '__main__':
    db = DataBase('../data/sql.db')
    db.create_table('new_table')
    db.list_tables()
    db.add_columns('new_table', {'col1': 'TEXT', 'col2': 'INTEGER', 'col3': 'REAL'})
    db.add_row('new_table', {'col1': 'ok', 'col2': 20})
    db.list_table_data('new_table')





