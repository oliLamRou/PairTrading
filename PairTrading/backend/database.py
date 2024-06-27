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

    def list_tables(self) -> list:
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return self.cursor.fetchall()

    def get_table(self, table_name: str) -> pd.DataFrame():
        return pd.read_sql_query(f"SELECT * FROM {table_name}", self.conn)

    def get_table_columns(self, table_name: str) -> list:
        self.cursor.execute(f'''PRAGMA table_info({table_name})''')
        columns = [col[1] for col in self.cursor.fetchall()]
        return columns

    def _drop_table(self, table_name: str):
        self.cursor.execute(f'DROP TABLE {table_name}')

    def clear_table(self, table_name: str):
        self.cursor.execute(f'DELETE FROM {table_name}')

    def create_table(self, table_name: str):
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY)'''
        )

    def add_columns(self,
            table_name: str, 
            columns: dict
        ):
        
        current_columns = self.get_table_columns(table_name)
        for column_name, column_type in columns.items():
            if column_name in current_columns:
                continue

            self.cursor.execute(f'''ALTER TABLE {table_name} ADD {column_name} {column_type}''') 
        
        self.conn.commit()
        self.get_table_columns(table_name)
        
    def add_row(self, table_name: str, row: dict):
        columns = ', '.join(str(key) for key in row.keys())
        values = tuple(row.values())
        placeholders = ', '.join('?' for _ in values)
        self.cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)
        self.conn.commit()

    def get_rows(self, table_name, column_name, value):
        self.cursor.execute(f"SELECT * FROM {table_name} WHERE {column_name} = ?", (value,))
        return self.cursor.fetchall()

if __name__ == '__main__':
    pass