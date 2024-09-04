import ast
from flask_restful import Resource, reqparse
from flask import request

from PairTrading.backend.wrangler.polygon_wrangler import PolygonWrangler
from PairTrading.backend.wrangler.user_wrangler import UserWrangler 
from PairTrading.backend.wrangler.yahoo_wrangler import YahooWrangler

class DataWrangler(Resource, YahooWrangler, PolygonWrangler, UserWrangler):
    def __init__(self):
        YahooWrangler.__init__(self)
        PolygonWrangler.__init__(self)
        UserWrangler.__init__(self)

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('pair_info')

    def get(self):
        if request.path == '/pair_info':
            tickers = request.args.getlist('tickers')
            if tickers:
                df = self.get_pair_info(tickers)
                return df.to_json()
        
        elif request.path == '/market_data':
            tickers = request.args.getlist('tickers')
            if tickers:
                df = self.market_data(tickers)
                return df.to_json(orient='records')
        
        elif request.path == '/company_info':
            industry = request.args.get('industry')
            if industry:
                sic_code = self.sic_code[self.sic_code['industry_title'] == industry].sic_code.iloc[0]
                company_info = self.all_ticker_info[self.all_ticker_info.sic_code == sic_code]
                return company_info.to_json(orient='records')
        
        else:
            print("ERROR")

    def put(self):
        args = self.parser.parse_args()
        pair_info = ast.literal_eval(args.get('pair_info'))
        df = self.update_pair_info(pair_info)