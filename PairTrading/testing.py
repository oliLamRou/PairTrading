import sqlite3
import pandas as pd

class DateBase:
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

    def create_table(self, columns):
        pass

    def get_df_from(self, table):
        pass


results = {'ticker': 'DNN', 'name': 'Denison Mines Corp', 'market': 'stocks', 'locale': 'us', 'primary_exchange': 'XASE', 'type': 'CS', 'active': True, 'currency_name': 'usd', 'cik': '0001063259', 'composite_figi': 'BBG000CX6DQ0', 'share_class_figi': 'BBG001S9ZPX7', 'market_cap': 1864819775.9399998, 'description': 'Denison Mines Corp is a uranium exploration and development company with interests focused in the Athabasca Basin region of northern Saskatchewan, Canada. The company has an effective 95% interest in its flagship Wheeler River Uranium Project, which is the largest undeveloped uranium project in the infrastructure-rich eastern portion of the Athabasca Basin region of northern Saskatchewan. The company is also engaged in mine decommissioning and environmental services through its Closed Mines group, which manages its Elliot Lake reclamation projects and provides third-party post-closure mine care and maintenance services.', 'ticker_root': 'DNN', 'homepage_url': 'https://www.denisonmines.com', 'total_employees': 64, 'list_date': '2007-04-19', 'branding': {'logo_url': 'https://api.polygon.io/v1/reference/company-branding/ZGVuaXNvbm1pbmVzLmNvbQ/images/2024-06-01_logo.png', 'icon_url': 'https://api.polygon.io/v1/reference/company-branding/ZGVuaXNvbm1pbmVzLmNvbQ/images/2024-06-01_icon.jpeg'}, 'share_class_shares_outstanding': 892000000, 'weighted_shares_outstanding': 892258266, 'round_lot': 100}

## Remove dict type
results_ = {}
for k, v in results.items():
    if type(results.get(k)) == dict:
        continue

    results_[k] = v

results = results_.copy()

def create_table(table_name):
    conn = sqlite3.connect('../data/pair_trading.db')
    c = conn.cursor()
    c.execute(f"create table if not exists {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT)")
    conn.commit()
    conn.close()

def list_tables():
    conn = sqlite3.connect('../data/pair_trading.db')
    c = conn.cursor()

    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    print(tables)

def insert():
    conn = sqlite3.connect('../data/pair_trading.db')
    c = conn.cursor()

    for column in results.keys():
        c.execute(f"PRAGMA table_info({table_name})")
        columns = [info[1] for info in c.fetchall()]
        if column not in columns:
            c.execute(f"ALTER TABLE {table_name} ADD COLUMN {column} TEXT")

    columns = ', '.join(results.keys())
    placeholders = ', '.join('?' for _ in results)
    values = tuple(results.values())
    print(values)

    c.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)

    # # Commit the changes and close the connection
    conn.commit()
    conn.close()


table_name = 'ticker_details'
# create_table(table_name)
# list_tables()

conn = sqlite3.connect('../data/pair_trading.db')
c = conn.cursor()
c.execute(f"PRAGMA table_info({table_name});")

# Fetch all results
columns_info = c.fetchall()
print(columns_info)

# Extract and print the column names
column_names = [info[1] for info in columns_info]
print("Columns in table:", table_name)
for name in column_names:
    print(name)