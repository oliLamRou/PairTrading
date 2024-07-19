import sqlite3
import pandas as pd

class DataBase:
    def __init__(self, path):
        self.path = path

    #READ
    def list_tables(self) -> pd.DataFrame():
        return self._read_sql_query("SELECT name FROM sqlite_master WHERE type='table'")

    def has_table(self, table_name) -> bool:
        conn = sqlite3.connect(self.path)
        query = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?", 
            conn, 
            params=(table_name,)
        )
        conn.close()
        return False if query.empty else True

    def get_rows(self, table_name: str, column_name: str, values: list) -> pd.DataFrame():
        values = "'" + "', '".join(values) + "'"
        return self._read_sql_query(
            f"SELECT * FROM {table_name} WHERE {column_name} IN ({values})"
        )

    def has_value(self, table_name, column_name, value) -> bool:
        query = self.get_rows(table_name, column_name, [value])
        return False if query.empty else True

    def get_table(self, table_name: str) -> pd.DataFrame():
        return self._read_sql_query(f"SELECT * FROM {table_name}")

    def get_table_columns(self, table_name: str) -> pd.DataFrame():
        return self._read_sql_query(f"PRAGMA table_info({table_name})")['name']

    def _read_sql_query(self, query):
        conn = sqlite3.connect(self.path)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    #WRITE
    @property
    def _vacuum(self):
        self._execute("VACUUM")

    def setup_table(self, table_name: str, columns: dict):
        self.create_table(table_name)
        self.add_columns(table_name, columns)

    def clear_table(self, table_name: str):
        self._execute(f'DELETE FROM {table_name}')

    def create_table(self, table_name: str):
        self._execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY)'''
        )

    def add_columns(self, table_name: str, columns: dict):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        current_columns = self.get_table_columns(table_name)
        for column_name, column_type in columns.items():
            if column_name in current_columns.values:
                continue

            print(f'Adding {column_name} of type: {column_type} in table: {table_name}')
            cursor.execute(f'''ALTER TABLE {table_name} ADD {column_name} {column_type}''')

        conn.commit()
        conn.close()
        
    def add_row(self, table_name: str, row: dict):
        columns = ', '.join(str(key) for key in row.keys())
        values = tuple(row.values())
        placeholders = ', '.join('?' for _ in values)
        self._execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values=values)

    def update_row(self, table_name: str, row: dict, column_name: str, column_value):
        columns = '=?, '.join(row.keys()) + '=?'
        values = list(row.values())
        values.append(column_value)
        self._execute(f'''UPDATE {table_name} SET {columns} WHERE {column_name} = ? ''', values=tuple(values))

    #DELETE
    def _drop_table(self, table_name: str):
        self._execute(f'DROP TABLE {table_name}')

    def _delete_rows(self, table_name: str, column_name: str, values: list):
        values = "'" + "', '".join(values) + "'"
        self._execute(f'DELETE FROM {table_name} WHERE {column_name} IN ({values})')

    def _execute(self, query, values=None):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)

        conn.commit()
        conn.close()

if __name__ == '__main__':
    from PairTrading.src import _constant
    db = DataBase('../../data/polygon.db')
    pair_info = {
        'A': 'AAPL',
        'B': 'MSTR'
    }
    # db.add_row('watchlist', pair_info)
    print(db.get_table('ticker_details'))


