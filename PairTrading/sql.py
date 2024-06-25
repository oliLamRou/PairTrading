import sqlite3
import pandas as pd

conn = sqlite3.connect('../data/sql.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS table1 
    (
        id INTEGER PRIMARY KEY, 
        name TEXT, 
        position TEXT, 
        salary REAL,
        bonus INTEGER
    )
''')
conn.commit()

c.execute('''PRAGMA table_info(table1)''')
[col[1] for col in c.fetchall()]

# c.execute('''
#     ALTER TABLE table1 ADD new INT
# ''') 
# conn.commit()


# c.execute("INSERT INTO table1 (name, salary, position) VALUES (?, ?, ?)", ('John Doe', 80000, 'Software Engineer'))
# conn.commit()

# df = pd.read_sql_query("SELECT * FROM table1", conn).drop(columns=['id'])
# print(df)

# results = {'ticker': 'DNN', 'name': 'Denison Mines Corp', 'market': 'stocks', 'locale': 'us', 'primary_exchange': 'XASE', 'type': 'CS', 'active': True, 'currency_name': 'usd', 'cik': '0001063259', 'composite_figi': 'BBG000CX6DQ0', 'share_class_figi': 'BBG001S9ZPX7', 'market_cap': 1864819775.9399998, 'description': 'Denison Mines Corp is a uranium exploration and development company with interests focused in the Athabasca Basin region of northern Saskatchewan, Canada. The company has an effective 95% interest in its flagship Wheeler River Uranium Project, which is the largest undeveloped uranium project in the infrastructure-rich eastern portion of the Athabasca Basin region of northern Saskatchewan. The company is also engaged in mine decommissioning and environmental services through its Closed Mines group, which manages its Elliot Lake reclamation projects and provides third-party post-closure mine care and maintenance services.', 'ticker_root': 'DNN', 'homepage_url': 'https://www.denisonmines.com', 'total_employees': 64, 'list_date': '2007-04-19', 'branding': {'logo_url': 'https://api.polygon.io/v1/reference/company-branding/ZGVuaXNvbm1pbmVzLmNvbQ/images/2024-06-01_logo.png', 'icon_url': 'https://api.polygon.io/v1/reference/company-branding/ZGVuaXNvbm1pbmVzLmNvbQ/images/2024-06-01_icon.jpeg'}, 'share_class_shares_outstanding': 892000000, 'weighted_shares_outstanding': 892258266, 'round_lot': 100}

# ## Remove dict type
# results_ = {}
# for k, v in results.items():
#     print(type(v))
#     if type(v) == dict:
#         results_[k] = str(v)
#         continue

#     results_[k] = v

# results = results_.copy()

# from pprint import pprint
# pprint(results)

# [
#     'ticker', 
#     'name', 
#     'market', 
#     'locale', 
#     'primary_exchange', 
#     'type', 
#     'active', 
#     'currency_name', 
#     'cik', 
#     'composite_figi', 
#     'share_class_figi', 
#     'market_cap', 
#     'description', 
#     'ticker_root', 
#     'homepage_url', 
#     'total_employees', 
#     'list_date', 'branding', 
#     'share_class_shares_outstanding', 
#     'weighted_shares_outstanding', 
#     'round_lot'
# ]




