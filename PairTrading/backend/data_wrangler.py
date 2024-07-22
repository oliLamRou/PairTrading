from PairTrading.backend.wrangler.polygon_wrangler import PolygonWrangler
from PairTrading.backend.wrangler.user_wrangler import UserWrangler 
from PairTrading.backend.wrangler.yahoo_wrangler import YahooWrangler

class DataWrangler(YahooWrangler, PolygonWrangler, UserWrangler):
    def __init__(self):
        YahooWrangler.__init__(self)
        PolygonWrangler.__init__(self)
        UserWrangler.__init__(self)

if __name__ == '__main__':
    dw = DataWrangler()