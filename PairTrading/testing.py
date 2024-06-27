from PairTrading.backend.polygon import Polygon


p = Polygon()
df = p.get_table('ticker_details')

print(df[df.ticker == 'MARA'])
