from PairTrading.backend.polygon import Polygon

p = Polygon()
df = p.get_table('day_AA')
print(df)
p.ticker_details("AAPL")
#print(p.list_tables())