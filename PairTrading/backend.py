import pandas as pd
from flask import Flask, request
from flask_cors import CORS
from PairTrading.backend.scanner import Scanner
from PairTrading.backend.ibkr import IBClient
from ibapi.client import Contract
from threading import Thread
import time

app = Flask(__name__)
CORS(app)

s = Scanner()
count = 0
ib = IBClient()

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
        print('BACKEND', df)
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
    pairInfo = request.json.get('pairInfo')
    if not pairInfo:
        return {}

    df = s.update_pair_info(pairInfo)
    return df.to_json()

@app.route('/ibkr_connect', methods=['GET'])
def ibkr_connect():
    global count
    global ib
    print(ib)
    ib_thread = Thread(target=ib.run)
    ib_thread.start()
    ib.connect('127.0.0.1', 7497, count)
    
    print("connect")
    print(count)
    count+=1
    return ""

@app.route('/ibkr_disconnect', methods=['GET'])
def ibkr_disconnect():
    global ib
    ib.data = []
    ib.disconnect()
    print('IB disconnected')
    return ""

@app.route('/ibkr_register_live_data', methods=['GET'])
def ibkr_register_live_data():
    global ib
    contract = Contract()
    contract.symbol = "AAPL"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    # Request live market data
    ib.reqMktData(ib.next_id(), contract, "232", False, False, [])

    # Sleep while receiving live data
    time.sleep(2)
    print(str(ib._data_buffer))
    return str(ib._data_queue)

@app.route('/ibkr_get_historical_data', methods=['GET'])
def ibkr_get_historical_data():
    global ib
    contract = Contract()
    contract.symbol = "AAPL"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    # Request historical data
    ib.reqHistoricalData(ib.next_id(), contract, "20240820 16:00:00 US/Eastern", "2 D", "1 min", "TRADES", 1, 1, False, [])

    # Sleep while receiving live data
    time.sleep(0.7)
    print(str(ib.historical_data))
    return ib.historical_data
    
app.run(debug=True, port=5002)