import sqlite3
import pandas as pd

class DataBase:
    def __init__(self, path):
        self.path = path
        # self.conn = conn
        # self.cursor = self.conn.cursor()


    # @property
    # def conn(self):
    #     return sqlite3.connect(self.path)

    # @property
    # def cursor(self):
    #     return self.conn.cursor()

    #READ
    def list_tables(self) -> pd.DataFrame():
        conn = sqlite3.connect(self.path)
        df = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", conn)
        conn.close()
        return df

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
        conn = sqlite3.connect(self.path)
        values = "'" + "', '".join(values) + "'"
        query = f"SELECT * FROM {table_name} WHERE {column_name} IN ({values})"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def has_value(self, table_name, column_name, value) -> bool:
        query = self.get_rows(table_name, column_name, [value])
        return False if query.empty else True

    def get_table(self, table_name: str) -> pd.DataFrame():
        conn = sqlite3.connect(self.path)
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        conn.close()
        return df

    def get_table_columns(self, table_name: str) -> pd.DataFrame():
        conn = sqlite3.connect(self.path)
        df = pd.read_sql_query(f"PRAGMA table_info({table_name})", conn)['name']
        conn.close()
        return df

    #WRITE
    @property
    def _commit(self):
        conn = sqlite3.connect(self.path)
        conn.commit()
    
    @property
    def _vacuum(self):
        conn = sqlite3.connect(self.path)
        conn.execute("VACUUM")
        conn.close()

    def setup_table(self, table_name: str, columns: dict):
        self.create_table(table_name)
        self.add_columns(table_name, columns)

    def clear_table(self, table_name: str):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute(f'DELETE FROM {table_name}')
        conn.close()

    def create_table(self, table_name: str):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY)'''
        )
        conn.close()

    def add_columns(self, table_name: str, columns: dict):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        current_columns = self.get_table_columns(table_name)
        for column_name, column_type in columns.items():
            if column_name in current_columns.values:
                continue

            print(f'Adding {column_name} of type: {column_type} in table: {table_name}')
            cursor.execute(f'''ALTER TABLE {table_name} ADD {column_name} {column_type}''')

        conn.close()
        
    def add_row(self, table_name: str, row: dict):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        columns = ', '.join(str(key) for key in row.keys())
        values = tuple(row.values())
        placeholders = ', '.join('?' for _ in values)
        cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)
        conn.close()

    def update_row(self, table_name: str, row: dict, column_name: str, column_value):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        columns = '=?, '.join(row.keys()) + '=?'
        values = list(row.values())
        values.append(column_value)
        cursor.execute(f'''UPDATE {table_name} SET {columns} WHERE {column_name} = ? ''', tuple(values))
        conn.close()

    #DELETE
    def _drop_table(self, table_name: str):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute(f'DROP TABLE {table_name}')
        conn.close()

    def _delete_rows(self, table_name: str, column_name: str, values: list):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        values = "'" + "', '".join(values) + "'"
        cursor.execute(f'DELETE FROM {table_name} WHERE {column_name} IN ({values})')
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


