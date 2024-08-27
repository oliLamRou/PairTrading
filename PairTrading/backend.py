import pandas as pd
from flask import Flask, request
from flask_cors import CORS
from PairTrading.backend.scanner import Scanner
from PairTrading.backend.data_wrangler import DataWrangler
from PairTrading.backend.ibkr import IBClient
from ibapi.client import Contract
from ibapi.order import Order
from ib_insync import *

from threading import Thread
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)

s = Scanner()
dw = DataWrangler()

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
    ib_connect()
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

@app.route('/ibkr_get_market_data', methods=['GET'])
def ibkr_get_market_data():
    ticker = request.args.get('ticker')

    global ib
    contract = Contract()
    contract.symbol = ticker
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    # Request market data
    req_id = ib.next_id()
    ib.reqMktData(req_id, contract, "", True, False, [])

    # Sleep while receiving live data
    time.sleep(0.6)
    #print(str(ib.get_data(req_id)))
    return str(ib.get_data(req_id))

@app.route('/ibkr_get_historical_data', methods=['GET'])
def ibkr_get_historical_data():
    ticker = request.args.get('ticker')
    size = request.args.get('size')
    length = request.args.get('length')

    print('TICKER: ', ticker, size, length)

    if ticker is None:
        return []

    contract = Contract()
    contract.symbol = ticker
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    global ib
    req_id = ib.next_id()
    ib.reqHistoricalData(req_id, contract, "", length, size, "TRADES", 1, 1, False, [])

    # Sleep while receiving live data
    time.sleep(0.7)
    data = ib.get_data(req_id)
    #print(data)
    return data
    
@app.route('/get_watchlist', methods=['GET'])
def get_watchlist():
    df = dw.get_pairs_in_watchlist('watchlist')
    return df.to_json(orient='records')

@app.route('/ibkr_place_order', methods=['GET'])
def ibkr_place_order():
    ticker = request.args.get('ticker')
    quantity = request.args.get('quantity')
    price = request.args.get('price')
    action = request.args.get('action')
    orderType = request.args.get('orderType')

    print('Place Order: ', ticker, quantity, price, action, orderType)

    if ticker is None:
        return []

    contract = Contract()
    contract.symbol = ticker
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    order = Order()
    order.totalQuantity = quantity
    order.action = action
    order.orderType = orderType
    order.eTradeOnly = False
    order.firmQuoteOnly = False
    if orderType == 'LMT':
        order.lmtPrice = price

    global ib
    req_id = ib.next_id()
    ib.placeOrder(req_id, contract, order)

    return req_id

@app.route('/ibkr_order_status', methods=['GET'])
def ibkr_order_status():
    id = request.args.get('id')

    print('Order Status: ', id)

    if id is None:
        return []

    global ib
    req_id = ib.next_id()
    ib.orderStatus(req_id, id)

    return req_id

def ib_connect():
    global count
    global ib

    ib_thread = Thread(target=ib.run)
    ib_thread.start()

    ib.connect('127.0.0.1', 7497, count)
    time.sleep(1)
    
    print("Try to connect, id: ", count)
    count+=1

app.run(debug=True, port=5002)