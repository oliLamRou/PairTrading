import pandas as pd
from flask import Flask, request
from flask_cors import CORS

from PairTrading.backend.scanner import Scanner
from PairTrading.backend.data_wrangler import DataWrangler

app = Flask(__name__)
CORS(app)

s = Scanner()
dw = DataWrangler()

@app.route('/get_potential_pair', methods=['GET'])
def get_potential_pair():
    df = s.potential_pair.sort_values('potential_pair', ascending=False)
    return df.to_json(orient='records')

@app.route('/get_pairs', methods=['GET'])
def get_pairs():
    min_price = request.args.get('min_price', type=float)
    if min_price:
        s.min_price = min_price

    max_price = request.args.get('max_price', type=float)
    if max_price:
        s.max_price = max_price

    min_volume = request.args.get('min_volume', type=float)
    if min_volume:
        s.min_vol = min_volume

    max_volume = request.args.get('max_volume', type=float)
    if max_volume:
        s.max_vol = max_volume

    industry = request.args.get('industry')
    if industry:
        s.industry = industry
        df = s.get_pairs()
        return df.to_json(orient='records')

    return {}

@app.route('/get_market_data', methods=['GET'])
def market_data():
    tickers = request.args.getlist('tickers')
    df = s.market_data(tickers)
    return df.to_json(orient='records')

@app.route('/company_info', methods=['GET'])
def company_info():
    industry = request.args.get('industry')
    if industry:
        sic_code = s.sic_code[s.sic_code['industry_title'] == industry].sic_code.iloc[0]
        company_info = s.all_ticker_info[s.all_ticker_info.sic_code == sic_code]
        return company_info.to_json(orient='records')

        
@app.route('/get_pair_info', methods=['GET'])
def pair_info():
    tickers = request.args.getlist('tickers')
    df = s.get_pair_info(tickers)

    return df.to_json()

@app.route('/update_pair_info', methods=['POST'])
def update_pair_info():
    tickers = request.json.get('tickers')
    pairInfo = request.json.get('pairInfo')
    if not tickers:
        return {}

    df = s.update_pair_info(tickers, pairInfo)
    return df.to_json()    
    
@app.route('/get_watchlist', methods=['GET'])
def get_watchlist():
    df = dw.get_pairs_in_watchlist('watchlist')
    return df.to_json(orient='records')

app.run(debug=True, port=5002)