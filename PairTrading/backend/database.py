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
    def list_tables(self) -> pd.DataFrame():
        return pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", self.conn)

    def has_table(self, table_name) -> bool:
        query = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?", 
            self.conn, 
            params=(table_name,)
        )
        return False if query.empty else True

    def get_rows(self, table_name, column_name, value) -> pd.DataFrame():
        return pd.read_sql_query(
            f"SELECT * FROM {table_name} WHERE {column_name} = ?", 
            self.conn, 
            params=(value,)
        )

    def has_value(self, table_name, column_name, value) -> bool:
        query = self.get_rows(table_name, column_name, value)
        return False if query.empty else True

    def get_table(self, table_name: str) -> pd.DataFrame():
        return pd.read_sql_query(f"SELECT * FROM {table_name}", self.conn)

    def get_table_columns(self, table_name: str) -> pd.DataFrame():
        return pd.read_sql_query(f"PRAGMA table_info({table_name})", self.conn)['name']

    #WRITE
    @property
    def _commit(self):
        self.conn.commit()
    
    def _vacuum(self):
        self.conn.execute("VACUUM")

    def setup_table(self, table_name: str, columns: dict):
        self.create_table(table_name)
        self.add_columns(table_name, columns)

    def clear_table(self, table_name: str):
        self.cursor.execute(f'DELETE FROM {table_name}')

    def create_table(self, table_name: str):
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY)'''
        )

    def add_columns(self, table_name: str, columns: dict):
        current_columns = self.get_table_columns(table_name)
        for column_name, column_type in columns.items():
            if column_name in current_columns.values:
                continue

            print(f'Adding {column_name} of type: {column_type} in table: {table_name}')
            self.cursor.execute(f'''ALTER TABLE {table_name} ADD {column_name} {column_type}''')
        
    def add_row(self, table_name: str, row: dict):
        columns = ', '.join(str(key) for key in row.keys())
        values = tuple(row.values())
        placeholders = ', '.join('?' for _ in values)
        self.cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)

    def update_row(self, table_name: str, row: dict, column_name: str, column_value):
        columns = '=?, '.join(row.keys()) + '=?'
        values = list(row.values())
        values.append(column_value)
        self.cursor.execute(f'''UPDATE {table_name} SET {columns} WHERE {column_name} = ? ''', tuple(values))

    #DELETE
    def _drop_table(self, table_name: str):
        self.cursor.execute(f'DROP TABLE {table_name}')

    def _delete_rows(self, table_name: str, column_name: str, column_value):
        self.cursor.execute(f'''DELETE FROM {table_name} WHERE {column_name} = ? ''', (column_value, ))

if __name__ == '__main__':
    from PairTrading.src import _constant
    db = DataBase('../../data/polygon.db')

    df = db.get_table('ticker_details')
    print(df.ticker)


