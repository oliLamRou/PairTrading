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

    #READ
    def list_tables(self) -> list:
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return self.cursor.fetchall()

    def table_exists(self, table_name):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        return self.cursor.fetchone() is not None

    def has_value(self, table_name, column_name, value):
        self.cursor.execute("SELECT EXISTS(SELECT 1 FROM 'ticker_details' WHERE ticker = ?)", ('MSTR',))
        return True if self.cursor.fetchone()[0] == 1 else False

    def get_rows(self, table_name, column_name, value):
        self.cursor.execute(f"SELECT * FROM {table_name} WHERE {column_name} = ?", (value,))
        return self.cursor.fetchall()

    def get_table(self, table_name: str) -> pd.DataFrame():
        return pd.read_sql_query(f"SELECT * FROM {table_name}", self.conn)

    def get_table_columns(self, table_name: str) -> list:
        self.cursor.execute(f'''PRAGMA table_info({table_name})''')
        columns = [col[1] for col in self.cursor.fetchall()]
        return columns

    #MODIFY
    def setup_table(self, table_name: str, columns: dict):
        self.create_table(table_name)
        self.add_columns(table_name, columns)

    def _drop_table(self, table_name: str):
        self.cursor.execute(f'DROP TABLE {table_name}')

    def clear_table(self, table_name: str):
        self.cursor.execute(f'DELETE FROM {table_name}')

    def create_table(self, table_name: str):
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY)'''
        )

    def add_columns(self, table_name: str, columns: dict):
        current_columns = self.get_table_columns(table_name)
        for column_name, column_type in columns.items():
            if column_name in current_columns:
                continue

            print(f'Adding {column_name} of type: {column_type} in table: {table_name}')
            self.cursor.execute(f'''ALTER TABLE {table_name} ADD {column_name} {column_type}''')
        
        self.conn.commit()
        
    def add_row(self, table_name: str, row: dict):
        columns = ', '.join(str(key) for key in row.keys())
        values = tuple(row.values())
        placeholders = ', '.join('?' for _ in values)
        self.cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)
        self.conn.commit()

    def update_row(self, table_name: str, row: dict, column_name: str, column_value):
        columns = '=?, '.join(row.keys()) + '=?'
        values = list(row.values())
        values.append(column_value)
        self.cursor.execute(f'''UPDATE {table_name} SET {columns} WHERE {column_name} = ? ''', tuple(values))

    def _delete_row(self, table_name: str, column_name: str, column_value):
        self.cursor.execute(f'''DELETE FROM {table_name} WHERE {column_name} = ? ''', (column_value, ))
        self.conn.commit()

if __name__ == '__main__':
    s = "SELECT EXISTS(SELECT 1 FROM 'ticker_details' WHERE ticker = ?)"
    db = DataBase('../../data/polygon.db')
    # db._delete_row('ticker_details', 'ticker', 'MSTR')
    x = db.get_rows('ticker_details', 'ticker', 'MSTR')
    print(x)

