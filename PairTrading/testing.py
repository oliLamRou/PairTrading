import pandas as pd
from PairTrading.backend.polygon import Polygon


p = Polygon()


table_name = 'ticker_details'
df = p.get_table(table_name)
for t in df.ticker.value_counts():
	if t > 1:
		print(t)

column_name = 'ticker'
value = 'ZXIET'
# p.cursor.execute(f'DELETE FROM "{table_name}" WHERE "{column_name}" = ?', (value,))
# p.conn.commit()